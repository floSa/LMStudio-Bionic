"""Bibliothèque de mesures pour machine à GPU dédié : chargement (lms / API REST), VRAM et RAM réellement consommées,
vitesse de traitement du prompt et de génération, concurrence. Utilisée par les scripts gpu_*.py.

Prérequis : LM Studio lancé (serveur sur 127.0.0.1:1234), `lms` dans le PATH, `nvidia-smi`, paquet psutil.
Aucune mesure ne télécharge de modèle ; les modèles utilisés sont ceux déjà présents sur disque.
"""
import json
import os
import subprocess
import threading
import time
import urllib.error
import urllib.request

import psutil

BASE = os.environ.get("LMSTUDIO_URL", "http://127.0.0.1:1234")
ICI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ICI, "resultats")
PHRASE = "La production d'électricité repose sur un ensemble de procédés industriels complexes. "


def lms(*args, timeout=900):
    t0 = time.time()
    r = subprocess.run(["lms", *args], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    sortie = (r.stdout + r.stderr).replace("\x1b[?25l", "").replace("\x1b[?25h", "").replace("\x1b[K", "")
    # la barre de progression imprime des centaines de lignes : ne garder que les lignes utiles
    lignes = [l for l in sortie.replace("\r", "\n").split("\n") if l.strip() and not l.strip().startswith("Loading ")]
    return time.time() - t0, "\n".join(lignes), r.returncode


def api(chemin, corps=None, methode=None, timeout=900):
    data = json.dumps(corps).encode() if corps is not None else None
    req = urllib.request.Request(BASE + chemin, data=data, headers={"Content-Type": "application/json"}, method=methode)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read().decode() or "null")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def vram_utilisee_mib():
    r = subprocess.run(["nvidia-smi", "--query-gpu=memory.used,memory.total", "--format=csv,noheader,nounits"], capture_output=True, text=True)
    u, t = [int(x) for x in r.stdout.strip().split(",")]
    return u, t


def ram_moteur():
    """Mémoire (Go) des processus llama-server : jeu de travail et mémoire privée."""
    ws = priv = 0
    for p in psutil.process_iter(["name"]):
        if (p.info["name"] or "").lower().startswith("llama-server"):
            try:
                mi = p.memory_info()
                ws += mi.rss
                priv += getattr(mi, "private", mi.rss)
            except psutil.Error:
                pass
    return ws / 2**30, priv / 2**30


def ram_systeme_utilisee():
    vm = psutil.virtual_memory()
    return (vm.total - vm.available) / 2**30


def decharger():
    lms("unload", "--all")
    time.sleep(2)


class Ligne:
    """Référence de mémoire avant chargement (pour mesurer l'écart)."""

    def __init__(self):
        self.vram0, self.vram_tot = vram_utilisee_mib()
        self.ram0 = ram_systeme_utilisee()


def charger_lms(modele, gpu="max", ctx=8192, parallel=1, identifiant="bench", extra=()):
    base = Ligne()
    dt, sortie, code = lms("load", modele, "--gpu", str(gpu), "-c", str(ctx), "--parallel", str(parallel), "--identifier", identifiant, "-y", *extra)
    return {"ok": code == 0, "load_s": round(dt, 1), "sortie": sortie[-300:], "base": base}


def charger_api(modele, ctx=8192, parallel=1, flash_attention=None, eval_batch_size=None, offload_kv=None, num_experts=None):
    base = Ligne()
    corps = {"model": modele, "context_length": ctx, "parallel": parallel, "echo_load_config": True}
    if flash_attention is not None:
        corps["flash_attention"] = flash_attention
    if eval_batch_size is not None:
        corps["eval_batch_size"] = eval_batch_size
    if offload_kv is not None:
        corps["offload_kv_cache_to_gpu"] = offload_kv
    if num_experts is not None:
        corps["num_experts"] = num_experts
    t0 = time.time()
    code, rep = api("/api/v1/models/load", corps)
    return {"ok": code == 200, "load_s": round(time.time() - t0, 1), "reponse": rep, "base": base}


def memoire_apres(base):
    time.sleep(3)
    u, t = vram_utilisee_mib()
    ws, priv = ram_moteur()
    return {"vram_go": round((u - base.vram0) / 1024, 2), "ram_moteur_ws_go": round(ws, 2), "ram_moteur_privee_go": round(priv, 2),
            "ram_systeme_delta_go": round(ram_systeme_utilisee() - base.ram0, 2)}


def ps_json():
    r = subprocess.run(["lms", "ps", "--json"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def flux(modele, prompt, max_tokens, raisonnement="none", timeout=1800):
    """Requête en flux : TTFT, vitesse de génération, jetons du prompt et de la réponse (champ usage)."""
    corps = {"model": modele, "messages": [{"role": "user", "content": prompt}], "stream": True, "temperature": 0, "max_tokens": max_tokens,
             "stream_options": {"include_usage": True}}
    if raisonnement:
        corps["reasoning_effort"] = raisonnement
    def ouvrir(c):
        req = urllib.request.Request(BASE + "/v1/chat/completions", data=json.dumps(c).encode(), headers={"Content-Type": "application/json"})
        return urllib.request.urlopen(req, timeout=timeout)

    t0 = time.time()
    premier = None
    n = 0
    usage = None
    try:
        r_ = ouvrir(corps)
    except urllib.error.HTTPError:  # niveau de raisonnement refusé par ce modèle : on réessaie sans
        corps.pop("reasoning_effort", None)
        r_ = ouvrir(corps)
    with r_ as r:
        for ligne in r:
            ligne = ligne.decode().strip()
            if not ligne.startswith("data:") or ligne.endswith("[DONE]"):
                continue
            ch = json.loads(ligne[5:])
            if ch.get("usage"):
                usage = ch["usage"]
            if ch.get("choices"):
                d = ch["choices"][0]["delta"]
                if d.get("content") or d.get("reasoning_content") or d.get("reasoning"):
                    if premier is None:
                        premier = time.time() - t0
                    n += 1
    fin = time.time() - t0
    toks = (usage or {}).get("completion_tokens", n)
    return {"ttft": premier, "total": fin, "tokens_sortie": toks, "tokens_prompt": (usage or {}).get("prompt_tokens"),
            "decode_tok_s": (toks - 1) / (fin - premier) if premier and toks > 1 and fin > premier else None}


def prompt_long(cible_tokens, tok_par_phrase=17):
    return PHRASE * max(1, cible_tokens // tok_par_phrase)


def mesurer(modele, parallel=1, longueurs=(2000,), gen_tokens=200):
    """Vitesse de traitement du prompt (une valeur par longueur), de génération, et débit sous concurrence."""
    res = {}
    flux(modele, "ok", 3)  # échauffement
    for L in longueurs:
        pp = flux(modele, prompt_long(L) + "\n\nRésume en une phrase.", 24)
        res[f"prompt_{L}"] = {"tokens": pp["tokens_prompt"], "ttft_s": round(pp["ttft"], 2) if pp["ttft"] else None,
                              "prompt_tok_s": round(pp["tokens_prompt"] / pp["ttft"], 1) if pp["ttft"] and pp["tokens_prompt"] else None}
    g = flux(modele, "Écris un paragraphe de 150 mots sur l'histoire de l'électricité.", gen_tokens)
    res["generation_tok_s"] = round(g["decode_tok_s"], 2) if g["decode_tok_s"] else None
    res["generation_tokens"] = g["tokens_sortie"]
    res["ttft_court_s"] = round(g["ttft"], 3) if g["ttft"] else None
    if parallel > 1:
        sorties = []

        def tr():
            sorties.append(flux(modele, "Écris un paragraphe de 150 mots sur l'histoire de l'électricité.", 150))

        ths = [threading.Thread(target=tr) for _ in range(parallel)]
        t0 = time.time()
        [t.start() for t in ths]
        [t.join() for t in ths]
        mur = time.time() - t0
        res["parallele"] = {"requetes": parallel, "debit_total_tok_s": round(sum(s["tokens_sortie"] for s in sorties) / mur, 2),
                            "par_requete_tok_s": round(sum((s["decode_tok_s"] or 0) for s in sorties) / len(sorties), 2)}
    return res


def sauver(nom, obj):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, nom), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)


def serialiser(d):
    """Retire l'objet Ligne (non sérialisable) d'un résultat de chargement."""
    return {k: v for k, v in d.items() if k != "base"}
