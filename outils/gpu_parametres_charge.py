"""Effet des paramètres de chargement sur la vitesse et la mémoire réelles (GPU dédié, moteur CUDA) :
parallélisme, Flash Attention, taille de lot d'évaluation, déchargement du cache K/V.
Modèle : Gemma 4 E4B (Q8_0). Chargement par l'API REST (`POST /api/v1/models/load`) ou `lms load`.
Résultats : outils/resultats/gpu_parametres_charge.json.

Usage : python gpu_parametres_charge.py [modele] [parallele|flash|lot|kv|tout]
"""
import json
import sys

from gpu_bench import *  # noqa: F401,F403

MODELE = sys.argv[1] if len(sys.argv) > 1 else "google/gemma-4-e4b"
QUOI = sys.argv[2] if len(sys.argv) > 2 else "tout"
resultats = []


def un_essai(etiquette, chargement, parallel=1, longueurs=(2000,)):
    decharger()
    ch = chargement()
    ligne = {"essai": etiquette, **serialiser(ch)}
    if ch["ok"]:
        ligne["memoire"] = memoire_apres(ch["base"])
        ligne["mesures"] = mesurer(MODELE if "reponse" in ch else "bench", parallel=parallel, longueurs=longueurs)
    resultats.append(ligne)
    sauver("gpu_parametres_charge.json", resultats)
    m = ligne.get("mesures", {})
    print(etiquette, "| load", ligne["load_s"], "s | mem", ligne.get("memoire"), "| mesures", json.dumps(m, ensure_ascii=False), flush=True)


if QUOI in ("parallele", "tout"):
    for p in (1, 2, 4, 8):
        un_essai(f"parallel={p}", lambda p=p: charger_lms(MODELE, "max", 8192, p), parallel=p)

if QUOI in ("flash", "tout"):
    for ctx in (8192, 65536):
        for fa in (True, False):
            un_essai(f"flash_attention={fa}, ctx={ctx}", lambda fa=fa, ctx=ctx: charger_api(MODELE, ctx, 1, flash_attention=fa),
                     longueurs=(2000, 6000) if ctx > 8192 else (2000,))

if QUOI in ("lot", "tout"):
    for b in (128, 512, 2048, 8192):
        un_essai(f"eval_batch_size={b}", lambda b=b: charger_api(MODELE, 16384, 1, eval_batch_size=b), longueurs=(2000, 6000))

if QUOI in ("kv", "tout"):
    for kv in (True, False):
        un_essai(f"offload_kv_cache_to_gpu={kv}, ctx=32768", lambda kv=kv: charger_api(MODELE, 32768, 1, offload_kv=kv), longueurs=(2000, 6000))

decharger()
print("terminé", flush=True)
