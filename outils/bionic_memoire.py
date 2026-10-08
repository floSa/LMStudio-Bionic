"""Mesure la mémoire occupée par un modèle chargé par Bionic (ajustement automatique AutoFit) : contexte chargé, VRAM, RAM du moteur.

Déroulé : décharge tous les modèles (`lms unload --all`), relève la VRAM de base, lance une courte tâche Bionic avec le modèle demandé
(chargement à la demande), puis relève `lms ps`, la VRAM (nvidia-smi) et la mémoire du processus `llama-server` (psutil).
Prérequis : voir bionic_tache.py ; `lms` dans le PATH ; Bionic expose le serveur local de LM Studio (port 1234).
Usage : python bionic_memoire.py "Gemma 4 E4B" Désactivé e4b
Résultat : outils/resultats/gpu_dedie/bionic_memoire_<étiquette>.json
"""
import json
import os
import subprocess
import sys
import time

import psutil

ICI = os.path.dirname(os.path.abspath(__file__))
modele, effort, etiquette = sys.argv[1], sys.argv[2], sys.argv[3]


def vram_mib():
    sortie = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"], capture_output=True, text=True).stdout
    return int(sortie.strip().splitlines()[0])


def moteur():
    """Mémoire (Go) du ou des processus llama-server : mémoire physique (working set) et privée."""
    ws = priv = 0
    for p in psutil.process_iter(["name"]):
        if "llama-server" in (p.info["name"] or ""):
            mi = p.memory_info()
            ws += mi.rss
            priv += getattr(mi, "private", mi.rss)
    return round(ws / 2**30, 2), round(priv / 2**30, 2)


def lms_ps():
    sortie = subprocess.run(["lms", "ps", "--json"], capture_output=True, text=True, encoding="utf-8").stdout
    return [{k: m.get(k) for k in ("modelKey", "sizeBytes", "contextLength", "parallel", "quantization")} for m in json.loads(sortie or "[]")]


subprocess.run(["lms", "unload", "--all"], capture_output=True)
time.sleep(6)
base = vram_mib()
base_ws, base_priv = moteur()
t0 = time.time()
sous = subprocess.run([sys.executable, os.path.join(ICI, "bionic_tache.py"), "--projet", "Démo documents", "--modele", modele, "--effort", effort,
                       "--etiquette", f"memoire_{etiquette}", "--consigne", "Réponds uniquement par le mot OK.", "--delai", "900"],
                      capture_output=True, text=True, encoding="utf-8", errors="replace",
                      env={**os.environ, "PYTHONIOENCODING": "utf-8"})
duree = round(time.time() - t0)
time.sleep(5)
apres = vram_mib()
ws, priv = moteur()
res = {"modele": modele, "effort": effort, "duree_tache_s": duree, "vram_base_mib": base, "vram_apres_mib": apres,
       "vram_modele_go": round((apres - base) / 1024, 2), "moteur_ws_go": ws, "moteur_prive_go": priv, "lms_ps": lms_ps(),
       "sortie_tache": sous.stdout[-300:]}
with open(os.path.join(ICI, "resultats", "gpu_dedie", f"bionic_memoire_{etiquette}.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "sortie_tache"}, ensure_ascii=False))
