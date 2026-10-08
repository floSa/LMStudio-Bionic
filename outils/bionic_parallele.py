"""Sessions Bionic simultanées : lance N sessions identiques (rédaction d'un texte court) l'une après l'autre, sans attendre la fin de la précédente,
puis mesure la durée totale jusqu'à la fin de toutes.

Usage : python bionic_parallele.py "Gemma 4 E4B" Désactivé N etiquette
Résultat : outils/resultats/gpu_dedie/bionic_parallele_<étiquette>.json (durée totale, modèle réel de chaque session)
Prérequis : voir bionic_tache.py. Ne jamais lancer un autre script de pilotage en même temps.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bionic_lib import choose_model, composer_click, connect, new_session  # noqa: E402
from lire_approbations_bionic import durees_sessions, modeles_sessions  # noqa: E402

ICI = os.path.dirname(os.path.abspath(__file__))
PID = "799ffbb4-5cbb-4aa1-8b99-6f909c8242ec"
modele, effort, n, etiquette = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
TACHE = "Écris un texte d'environ 1500 mots, structuré en dix parties numérotées, sur les avantages d'un modèle de langage utilisé en local. Réponds directement, sans utiliser d'outil."

lm = connect(1440, 900)
t_debut_ms = int(time.time() * 1000)
n0 = lm.text().count("Bionic a terminé sa réponse")
envois = []
for i in range(n):
    new_session(lm, "Démo documents")
    choose_model(lm, modele, effort)
    composer_click(lm)
    lm.type(TACHE); lm.wait(0.4)
    envois.append(time.time())
    lm.key("Enter")
    lm.wait(1.0)
t_premier = envois[0]
fin, ds = "délai", []
while time.time() - t_premier < 600:
    time.sleep(3)
    ds = [d for d in durees_sessions(PID, t_debut_ms) if d["t_utilisateur_ms"] >= t_debut_ms]
    if len(ds) >= n and all(d["terminee"] and d["t_assistant_ms"] > d["t_utilisateur_ms"] for d in ds):
        fin = "terminé"
        break
total = round((max(d["t_assistant_ms"] for d in ds) - min(d["t_utilisateur_ms"] for d in ds)) / 1000, 1) if ds else None
par_session = [round((d["t_assistant_ms"] - d["t_utilisateur_ms"]) / 1000, 1) for d in ds]
res = {"modele": modele, "sessions": n, "fin": fin, "duree_totale_s": total, "duree_par_session_s": par_session, "decalage_envois_s": [round(e - t_premier, 1) for e in envois],
       "modeles_reels": sorted({d["modele"] for d in ds})}
with open(os.path.join(ICI, "resultats", "gpu_dedie", f"bionic_parallele_{etiquette}.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False))
