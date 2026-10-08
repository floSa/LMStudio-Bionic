"""Paramètres de chargement accessibles seulement par le SDK (ou l'interface) : quantification du cache K/V, taille de lot physique,
experts MoE sur le CPU, décodage spéculatif. Chargement par `sdk_js/charger.mjs` (Node.js), mesure par l'API compatible OpenAI.
Résultats : outils/resultats/gpu_sdk_params_<ensemble>.json.

Usage : python gpu_sdk_params.py <kv|lot|moe|spec|spec_qwen>
"""
import json
import os
import subprocess
import sys

from gpu_bench import *  # noqa: F401,F403

QUOI = sys.argv[1] if len(sys.argv) > 1 else "kv"
SDK = os.path.join(ICI, "sdk_js")
E4B, MOE, DENSE = "google/gemma-4-e4b", "google/gemma-4-26b-a4b", "qwen/qwen3.8-27b"
resultats = []

CODE = "AZ-7741-QUARTZ"
MEULE = ("Rapport interne : le service comptable archive les pièces justificatives chaque trimestre. " * 20).strip()


def aiguille(n_tokens):
    """Texte long avec une information unique (« code secret ») au milieu ; la question porte sur cette information."""
    bloc = (MEULE + " ") * max(1, n_tokens // 340)
    moitie = len(bloc) // 2
    return bloc[:moitie] + f" NOTE IMPORTANTE : le code secret du coffre est {CODE}. " + bloc[moitie:] + "\n\nQuel est le code secret du coffre ? Réponds uniquement par le code."


def charger_sdk(modele, config, identifiant="bench"):
    base = Ligne()
    t0 = time.time()
    r = subprocess.run(["node", "charger.mjs", modele, identifiant, json.dumps(config)], cwd=SDK, capture_output=True, text=True, encoding="utf-8", timeout=900)
    try:
        sortie = json.loads(r.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        sortie = {"ok": False, "erreur": (r.stdout + r.stderr)[-300:]}
    return {"ok": bool(sortie.get("ok")), "load_s": round(time.time() - t0, 1), "sdk": sortie, "base": base}


def essai(etiquette, modele, config, longueurs=(2000, 6000), aiguille_tokens=None, gen_tokens=200):
    decharger()
    ch = charger_sdk(modele, config)
    ligne = {"essai": etiquette, "modele": modele, "config": config, **serialiser(ch)}
    if ch["ok"]:
        ligne["memoire"] = memoire_apres(ch["base"])
        try:
            ligne["mesures"] = mesurer("bench", longueurs=longueurs, gen_tokens=gen_tokens)
            if aiguille_tokens:
                f = flux("bench", aiguille(aiguille_tokens), 40)
                ligne["aiguille"] = {"tokens_prompt": f["tokens_prompt"], "ttft_s": round(f["ttft"], 2) if f["ttft"] else None}
                # relecture de la réponse (non streamée) pour vérifier le code
                code, rep = api("/v1/chat/completions", {"model": "bench", "messages": [{"role": "user", "content": aiguille(aiguille_tokens)}],
                                                          "max_tokens": 40, "temperature": 0, "reasoning_effort": "none"})
                txt = rep["choices"][0]["message"]["content"] if code == 200 else str(rep)[:200]
                ligne["aiguille"]["reponse"] = txt.strip()[:80]
                ligne["aiguille"]["trouve"] = CODE in txt
        except Exception as e:  # noqa: BLE001
            ligne["erreur_mesure"] = repr(e)
    resultats.append(ligne)
    sauver(f"gpu_sdk_params_{QUOI}.json", resultats)
    print(json.dumps(ligne, ensure_ascii=False, default=str), flush=True)


if QUOI == "kv":
    ctx = 65536
    base = {"contextLength": ctx, "flashAttention": True}
    for k, v in (("f16", "f16"), ("q8_0", "f16"), ("q8_0", "q8_0"), ("q4_0", "q4_0")):
        cfg = dict(base)
        if (k, v) != ("f16", "f16"):
            cfg["llamaKCacheQuantizationType"] = k
            cfg["llamaVCacheQuantizationType"] = v
        essai(f"K={k} V={v}, ctx {ctx}", E4B, cfg, aiguille_tokens=30000)
elif QUOI == "lot":
    for pb in (128, 256, 512, 1024, 2048):
        essai(f"physicalBatchSize={pb} (evalBatchSize=2048)", E4B, {"contextLength": 16384, "evalBatchSize": 2048, "physicalBatchSize": pb})
elif QUOI == "moe":
    ctx = 8192
    essai("26B A4B, automatique", MOE, {"contextLength": ctx})
    essai("26B A4B, GPU max imposé", MOE, {"contextLength": ctx, "gpu": {"ratio": "max"}})
    for n in (0, 8, 16, 30):
        essai(f"26B A4B, experts des {n} premières couches sur le CPU (--n-cpu-moe {n})", MOE,
              {"contextLength": ctx, "gpu": {"ratio": "max"},
               "llamaCppArgumentsOverride": {"enabled": True, "disabledParameters": [], "excludeAllConfig": False,
                                             "overrideParameters": [{"key": "--n-cpu-moe", "value": str(n)}]}})
    essai("26B A4B, tous les experts sur le CPU (--cpu-moe)", MOE,
          {"contextLength": ctx, "gpu": {"ratio": "max"},
           "llamaCppArgumentsOverride": {"enabled": True, "disabledParameters": [], "excludeAllConfig": False,
                                         "overrideParameters": [{"key": "--cpu-moe", "value": ""}]}})
elif QUOI == "spec":
    essai("E4B sans décodage spéculatif", E4B, {"contextLength": 8192})
    essai("E4B, décodage spéculatif MTP", E4B, {"contextLength": 8192, "speculativeDraftMtp": True})
    essai("26B A4B (auto) sans décodage spéculatif", MOE, {"contextLength": 8192})
    essai("26B A4B (auto) avec brouillon E4B (Draft Simple)", MOE,
          {"contextLength": 8192, "speculativeDraftSimple": True, "speculativeDraftModel": E4B, "speculativeDraftMaxTokens": 8})
elif QUOI == "spec_qwen":
    # Qwen3.8 27B annonce un badge « MTP » : le modèle embarque une tête de prédiction multi-jetons
    essai("Qwen3.8 27B (auto) sans décodage spéculatif", DENSE, {"contextLength": 8192}, longueurs=(2000,))
    for n in (2, 4):
        essai(f"Qwen3.8 27B (auto), MTP, {n} jetons brouillon max", DENSE,
              {"contextLength": 8192, "speculativeDraftMtp": True, "speculativeDraftMaxTokens": n}, longueurs=(2000,))
    essai("Qwen3.8 27B (auto), MTP, réglages par défaut", DENSE, {"contextLength": 8192, "speculativeDraftMtp": True}, longueurs=(2000,))

decharger()
print("terminé", flush=True)
