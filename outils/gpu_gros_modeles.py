"""Modèles plus gros que la VRAM (16 Go) : chargement automatique ou à offload imposé, grand contexte, mémoire et vitesse réelles.
Modèles présents sur le disque : Gemma 4 E4B (Q8_0, 9 Go), Gemma 4 26B A4B (MoE, Q4_K_M, 18 Go), Qwen3.8 27B (dense, Q4_K_M, 17,7 Go).
Résultats : outils/resultats/gpu_gros_modeles.json.

Usage : python gpu_gros_modeles.py <ensemble>
  ensemble = e4b_contexte | moe | dense | moe_contexte | dense_contexte
"""
import json
import sys

from gpu_bench import *  # noqa: F401,F403

QUOI = sys.argv[1] if len(sys.argv) > 1 else "moe"
resultats = []


def estimation(modele, ctx):
    dt, sortie, code = lms("load", modele, "-c", str(ctx), "--estimate-only", "-y")
    return " | ".join(l.strip() for l in sortie.splitlines() if "Estimated" in l or "Confidence" in l)


def essai(etiquette, modele, gpu=None, ctx=8192, parallel=1, longueurs=(2000,), gen_tokens=200, raisonnement="none"):
    decharger()
    ligne = {"essai": etiquette, "modele": modele, "gpu": gpu, "ctx": ctx, "estimation_cli": estimation(modele, ctx)}
    base = Ligne()
    args = ["load", modele, "-c", str(ctx), "--parallel", str(parallel), "--identifier", "bench", "-y"]
    if gpu is not None:
        args += ["--gpu", str(gpu)]
    dt, sortie, code = lms(*args)
    ligne.update({"ok": code == 0, "load_s": round(dt, 1), "sortie": sortie[-200:]})
    if code == 0:
        ligne["memoire"] = memoire_apres(base)
        try:
            ligne["mesures"] = mesurer("bench", parallel=parallel, longueurs=longueurs, gen_tokens=gen_tokens)
        except Exception as e:  # noqa: BLE001
            ligne["erreur_mesure"] = repr(e)
    resultats.append(ligne)
    sauver(f"gpu_gros_modeles_{QUOI}.json", resultats)
    print(json.dumps(ligne, ensure_ascii=False), flush=True)


E4B, MOE, DENSE = "google/gemma-4-e4b", "google/gemma-4-26b-a4b", "qwen/qwen3.8-27b"

if QUOI == "e4b_contexte":
    for ctx in (8192, 32768, 131072):
        essai(f"E4B Q8_0, ctx {ctx}", E4B, "max", ctx, longueurs=(2000, 6000) if ctx > 8192 else (2000,))
elif QUOI == "moe":
    essai("26B A4B, offload automatique", MOE, None, 8192)
    for g in ("max", "0.75", "0.5", "off"):
        essai(f"26B A4B, offload {g}", MOE, g, 8192)
elif QUOI == "dense":
    essai("Qwen3.8 27B, offload automatique", DENSE, None, 8192)
    for g in ("max", "0.75", "0.5", "off"):
        essai(f"Qwen3.8 27B, offload {g}", DENSE, g, 8192)
elif QUOI == "moe_contexte":
    for ctx in (32768, 131072, 262144):
        essai(f"26B A4B, auto, ctx {ctx}", MOE, None, ctx, longueurs=(2000, 6000))
elif QUOI == "dense_contexte":
    for ctx in (32768, 131072, 262144):
        essai(f"Qwen3.8 27B, auto, ctx {ctx}", DENSE, None, ctx, longueurs=(2000, 6000))

decharger()
print("terminé", flush=True)
