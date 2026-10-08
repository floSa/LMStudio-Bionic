"""Essai libre dans une nouvelle session Bionic : saisie d'un texte (consigne ou commande `/`), attente de la fin, relevé du modèle réel, de la durée,
des outils appelés et de la réponse ; capture facultative.

Usage : python bionic_essai.py <projet> <modèle> <effort> <étiquette> <texte> [--mode "Vérification automatique"] [--entrees N] [--capture chemin.png] [--delai 300]
  --entrees N : nombre de pressions supplémentaires sur Entrée après le texte (menu `/` : une pression valide la commande, une seconde l'envoie)
Résultat : outils/resultats/gpu_dedie/bionic_<étiquette>.json
"""
import argparse
import base64
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bionic_lib import bouton_aria, choose_model, composer_click, connect, new_session, visible_at  # noqa: E402
from lire_approbations_bionic import commandes, modele_reel, resume  # noqa: E402

ICI = os.path.dirname(os.path.abspath(__file__))
PROJETS = {"Démo code": "41716555-c06b-4e4a-9b3c-3be762d6131d", "Démo jetable": "47c07a0a-b9e5-42f4-8442-f8ec0d10ffc2",
           "Démo documents": "799ffbb4-5cbb-4aa1-8b99-6f909c8242ec"}

p = argparse.ArgumentParser()
p.add_argument("projet"); p.add_argument("modele"); p.add_argument("effort"); p.add_argument("etiquette"); p.add_argument("texte")
p.add_argument("--mode"); p.add_argument("--entrees", type=int, default=0); p.add_argument("--capture"); p.add_argument("--delai", type=int, default=300)
p.add_argument("--oui-shell", action="store_true")
a = p.parse_args()

lm = connect(1440, 900)
new_session(lm, a.projet)
t_debut_ms = int(time.time() * 1000)
print("modèle :", choose_model(lm, a.modele, a.effort), flush=True)
if a.mode:
    pm = bouton_aria(lm, "Mode shell")
    lm.click_xy(*pm); lm.wait(1)
    pt = visible_at(lm, a.mode, 900)
    if pt:
        lm.click_xy(*pt); lm.wait(1)
    lm.key("Escape"); lm.wait(0.5)
composer_click(lm)
lm.type(a.texte); lm.wait(1.0)
n0 = lm.text().count("Bionic a terminé sa réponse")
t0 = time.time()
lm.key("Enter")
for _ in range(a.entrees):
    lm.wait(1.5); lm.key("Enter")
raison, journal = "délai dépassé", []
while time.time() - t0 < a.delai:
    time.sleep(3)
    t = lm.text()
    if "Votre agent souhaite exécuter des commandes shell" in t:
        pt = visible_at(lm, "Vérification manuelle" if a.mode == "Demander à chaque fois" else "Vérification automatique (recommandée)", 900)
        journal.append({"t": round(time.time() - t0), "autorisation_session": True})
        if pt:
            lm.click_xy(*pt); lm.wait(2); continue
    if "Action requise" in t or "Confirm shell command" in t:
        journal.append({"t": round(time.time() - t0), "action_requise": True})
        if a.oui_shell:
            pt = visible_at(lm, "Yes", 900, exact=True)
            if pt:
                lm.click_xy(*pt); lm.wait(2); continue
        raison = "action requise"; break
    if t.count("Bionic a terminé sa réponse") > n0:
        raison = "terminé"; break
duree = round(time.time() - t0)
lm.wait(1.5)
if a.capture:
    d = lm.send("Page.captureScreenshot", format="png")["data"]
    with open(a.capture, "wb") as f:
        f.write(base64.b64decode(d))
pid = PROJETS[a.projet]
try:
    outils, reponse = resume(pid, t_debut_ms)
except Exception as e:  # noqa: BLE001
    outils, reponse = None, repr(e)
res = {"etiquette": a.etiquette, "projet": a.projet, "modele": a.modele, "effort": a.effort, "mode": a.mode, "texte": a.texte, "fin": raison,
       "duree_mesuree_s": duree, "journal": journal, "outils_appeles": outils, "reponse_agent": reponse, "modele_reel": modele_reel(pid, t_debut_ms),
       "commandes": [{"commande": c["commande"], "approbation": c["approbation"], "erreur": c["erreur"]} for c in commandes(pid, depuis=t_debut_ms)]}
with open(os.path.join(ICI, "resultats", "gpu_dedie", f"bionic_{a.etiquette}.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print(json.dumps({k: res[k] for k in ("modele_reel", "fin", "duree_mesuree_s", "outils_appeles", "journal")}, ensure_ascii=False))
print(reponse)
