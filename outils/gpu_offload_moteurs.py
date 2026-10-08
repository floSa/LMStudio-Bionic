"""Vitesse et mémoire selon le moteur (CUDA / Vulkan / CPU) et le nombre de couches sur le GPU.
Modèle : Gemma 4 E4B (Q8_0, 9,02 Go), contexte 8 192, une requête à la fois.
Résultats : outils/resultats/gpu_offload_moteurs.json. Le moteur sélectionné au départ est rétabli à la fin.

Usage : python gpu_offload_moteurs.py [modele]
"""
import json
import subprocess
import sys

from gpu_bench import *  # noqa: F401,F403

MODELE = sys.argv[1] if len(sys.argv) > 1 else "google/gemma-4-e4b"
MOTEURS = [
    ("CUDA 12 (2.53.0)", "llama.cpp-win-x86_64-nvidia-cuda12-avx2@2.53.0", ["off", "0.25", "0.5", "0.75", "max"]),
    ("CUDA 12 (2.51.0)", "llama.cpp-win-x86_64-nvidia-cuda12-avx2@2.51.0", ["max"]),
    ("Vulkan (2.51.0)", "llama.cpp-win-x86_64-vulkan-avx2@2.51.0", ["off", "0.5", "max"]),
    ("CPU AVX2 (2.51.0)", "llama.cpp-win-x86_64-avx2@2.51.0", ["off"]),
]


def selection_actuelle():
    r = subprocess.run(["lms", "runtime", "ls"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return [l.split()[0] for l in r.stdout.splitlines() if "✓" in l]


if __name__ == "__main__":
    avant = selection_actuelle()
    print("moteurs sélectionnés au départ :", avant, flush=True)
    resultats = []
    try:
        for nom, moteur, gpus in MOTEURS:
            dt, sortie, code = lms("runtime", "select", moteur)
            print("select", moteur, code, sortie[-120:].replace("\n", " "), flush=True)
            for gpu in gpus:
                decharger()
                ch = charger_lms(MODELE, gpu=gpu, ctx=8192, parallel=1)
                ligne = {"moteur": nom, "gpu": gpu, **serialiser(ch)}
                if ch["ok"]:
                    ligne["memoire"] = memoire_apres(ch["base"])
                    ligne["mesures"] = mesurer("bench", longueurs=(2000,))
                resultats.append(ligne)
                print(json.dumps(ligne, ensure_ascii=False), flush=True)
                sauver("gpu_offload_moteurs.json", resultats)
    finally:
        decharger()
        for m in avant:
            if "executorch" in m:
                continue
            print("rétablissement", m, lms("runtime", "select", m)[1][-100:], flush=True)
        print("moteurs sélectionnés à la fin :", selection_actuelle(), flush=True)
