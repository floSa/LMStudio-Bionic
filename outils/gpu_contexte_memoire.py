"""Mémoire réellement consommée (VRAM, RAM) selon la taille de contexte pour Gemma 4 E4B (Q8_0), à comparer à l'estimation de LM Studio
(`lms load --estimate-only`). Aucune génération : chargement puis relevé. Résultats : outils/resultats/gpu_dedie/contexte_memoire.json."""
from gpu_bench import *  # noqa: F401,F403

MODELE = "google/gemma-4-e4b"
res = []
for ctx in (2048, 4096, 8192, 16384, 32768, 65536, 131072):
    decharger()
    dt, sortie, _ = lms("load", MODELE, "-c", str(ctx), "--estimate-only", "-y")
    est = [l.split(":")[1].strip() for l in sortie.splitlines() if "Estimated GPU" in l or "Estimated Total" in l]
    ch = charger_lms(MODELE, "max", ctx, 1)
    m = memoire_apres(ch["base"])
    res.append({"contexte": ctx, "estimation_gpu_total_gib": est, **m})
    print(res[-1], flush=True)
decharger()
sauver("gpu_dedie/contexte_memoire.json", res)
