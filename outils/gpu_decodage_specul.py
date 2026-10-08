"""Décodage spéculatif MTP (tête de prédiction multi-jetons embarquée) avec `lms load` : Qwen3.8 27B, offload automatique, contexte 8 192.
Compare la vitesse de génération sans et avec --speculative-draft-mtp, pour plusieurs longueurs de brouillon, sur deux types de texte.
Résultats : outils/resultats/gpu_decodage_specul.json."""
import json
from gpu_bench import *  # noqa: F401,F403

MODELE = "qwen/qwen3.8-27b"
resultats = []
PROMPTS = {"prose": "Écris un paragraphe de 150 mots sur l'histoire de l'électricité.",
           "code": "Écris en Python une fonction qui trie une liste de dictionnaires par la clé 'age' puis par la clé 'nom', avec docstring et deux exemples d'appel."}


def essai(etiquette, extra):
    decharger()
    base = Ligne()
    dt, sortie, code = lms("load", MODELE, "-c", "8192", "--identifier", "bench", "-y", *extra)
    ligne = {"essai": etiquette, "extra": list(extra), "ok": code == 0, "load_s": round(dt, 1), "sortie": sortie[-160:]}
    if code == 0:
        ligne["memoire"] = memoire_apres(base)
        flux("bench", "ok", 3)
        ligne["generation"] = {}
        for nom, p in PROMPTS.items():
            vit = []
            for _ in range(2):
                f = flux("bench", p, 200)
                vit.append(round(f["decode_tok_s"], 2) if f["decode_tok_s"] else None)
            ligne["generation"][nom] = vit
    resultats.append(ligne)
    sauver("gpu_decodage_specul.json", resultats)
    print(json.dumps(ligne, ensure_ascii=False), flush=True)


essai("sans décodage spéculatif", ["--no-speculative-draft-mtp"])
for n in (2, 3, 4, 8):
    essai(f"MTP, brouillon max {n}", ["--speculative-draft-mtp", "--speculative-draft-max-tokens", str(n)])
essai("MTP, réglages par défaut", ["--speculative-draft-mtp"])
decharger()
print("terminé")
