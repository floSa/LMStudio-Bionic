"""Bionic - captures et relevé de texte de toutes les pages de réglages (aucune connexion à un compte, aucun téléchargement)."""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lmcdp import LM

D = "bionic/02-reglages/"
lm = LM(port=9223, width=1440, height=900)
pages = [("Général", 88, "01-general"), ("Agent", 122, "02-agent"), ("Voix", 156, "03-voix"),
         ("Facturation et utilisation", 190, "04-facturation"), ("Apparence", 224, "05-apparence"), ("Sessions", 258, "06-sessions"),
         ("MCP", 332, "07-mcp"), ("Compétences", 366, "08-competences"), ("LM Link", 440, "09-lm-link"),
         ("Explorer", 513, "10-explorer"), ("Bibliothèque", 547, "11-bibliotheque"), ("Instances chargées", 581, "12-instances"),
         ("API des modèles locaux", 615, "13-api-modeles-locaux"), ("Paramètres par défaut des modèles locaux", 649, "14-parametres-defaut"),
         ("Moteur d’exécution", 683, "15-moteur")]
out = {}
for nom, y, fic in pages:
    lm.click_xy(100, y); lm.wait(2.5)
    txt = lm.ev("document.body.innerText").replace("\n\n", "\n")
    out[nom] = txt.split("Moteur d’exécution", 1)[-1] if nom != "Moteur d’exécution" else txt
    lm.shot(D + fic)
    print("ok", nom, flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resultats", "bionic_reglages_texte.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for nom, t in out.items():
    print("=" * 10, nom)
    print(t[:1800])
