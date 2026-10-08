"""Lance une tâche dans une nouvelle session Bionic, mesure la durée et enregistre le résultat (JSON + capture hors du dossier docs).

Prérequis : Bionic lancé avec --remote-debugging-port=9223, LM Studio fermé ; projets créés (voir outils/README.md).
Les confirmations « Confirm shell command » peuvent être acceptées automatiquement (--oui-shell) : à n'utiliser que dans un projet jetable.

Usage :
  python bionic_tache.py --projet "Démo code" --modele "Gemma 4 E4B" --effort Activé --etiquette bogue_e4b \
      --mode "Demander à chaque fois" --oui-shell --consigne "Exécute les tests, trouve la cause…"
Résultats : outils/resultats/gpu_dedie/bionic_<étiquette>.json
"""
import argparse
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bionic_lib import bouton_aria, choose_model, composer_click, connect, model_chip, new_session, visible_at  # noqa: E402
from lire_approbations_bionic import commandes, modele_reel, resume  # noqa: E402

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "resultats", "gpu_dedie")
PROJETS = {"Démo code": "41716555-c06b-4e4a-9b3c-3be762d6131d", "Démo jetable": "47c07a0a-b9e5-42f4-8442-f8ec0d10ffc2",
           "Démo documents": "799ffbb4-5cbb-4aa1-8b99-6f909c8242ec"}

p = argparse.ArgumentParser()
p.add_argument("--projet", required=True)
p.add_argument("--modele", required=True)
p.add_argument("--effort")
p.add_argument("--consigne", required=True)
p.add_argument("--fichiers", default="")
p.add_argument("--etiquette", required=True)
p.add_argument("--mode", help="Désactivé | Demander à chaque fois | Vérification automatique | Tout autoriser")
p.add_argument("--oui-shell", action="store_true")
p.add_argument("--delai", type=int, default=1500)
a = p.parse_args()

lm = connect(1440, 900)
new_session(lm, a.projet)
t_debut_ms = int(time.time() * 1000)

# modèle (vérifié sur le bouton ; lève RuntimeError sinon)
chip = choose_model(lm, a.modele, a.effort)
print("modèle :", chip, flush=True)

if a.mode:
    # le bouton « Mode shell » (aria-label) ouvre le choix du mode ; repéré dans la colonne de la nouvelle session
    pm = bouton_aria(lm, "Mode shell")
    if pm is None:
        raise LookupError("bouton Mode shell introuvable")
    lm.click_xy(*pm)
    lm.wait(1)
    pt = visible_at(lm, a.mode, 900)
    if pt:
        lm.click_xy(*pt); lm.wait(1)
    lm.key("Escape"); lm.wait(0.5)

if a.fichiers:
    lm.drop_files(a.fichiers.split(";"), x=670, y=500); lm.wait(1.5)

composer_click(lm)
lm.type(a.consigne); lm.wait(0.4)
n0 = lm.text().count("Bionic a terminé sa réponse")
t0 = time.time()
lm.key("Enter")
journal, raison = [], None
while time.time() - t0 < a.delai:
    time.sleep(3)
    t = lm.text()
    if "Votre agent souhaite exécuter des commandes shell" in t:
        # Bionic 1.1.7 : l'autorisation du shell se demande par session (boîte d'information), même quand un mode est déjà choisi
        choix = "Vérification manuelle" if a.mode == "Demander à chaque fois" else "Vérification automatique (recommandée)"
        pt = visible_at(lm, choix, 900)
        journal.append({"t": round(time.time() - t0), "autorisation_session": choix})
        print("autorisation du shell par session :", choix, flush=True)
        if pt:
            lm.click_xy(*pt); lm.wait(2)
            continue
    if "Action requise" in t or "Confirm shell command" in t:
        cmd = lm.ev(r"""(()=>{const e=[...document.querySelectorAll('body *')].filter(x=>x.children.length===0 && /Do you want to run/.test(x.innerText||'')); return e.length? e[e.length-1].innerText : null})()""")
        journal.append({"t": round(time.time() - t0), "demande": cmd})
        print("confirmation demandée :", cmd, flush=True)
        if a.oui_shell:
            pt = visible_at(lm, "Yes", 900, exact=True)
            if pt:
                lm.click_xy(*pt); lm.wait(2)
                continue
        raison = "action requise"
        break
    if t.count("Bionic a terminé sa réponse") > n0:
        raison = "terminé"
        break
duree = round(time.time() - t0)
lm.wait(1.5)
vt = lm.visible_text()
# la durée affichée suit directement le texte de la consigne dans l'onglet actif (les autres onglets restent dans le DOM)
ms = re.findall(re.escape(a.consigne[-25:]) + r"\s*Travail effectué en ([^\n]+)", vt)
m = ms[-1] if ms else None
res = {"etiquette": a.etiquette, "projet": a.projet, "modele": a.modele, "effort": a.effort, "mode": a.mode, "consigne": a.consigne,
       "fin": raison, "duree_mesuree_s": duree, "duree_affichee": m, "confirmations": journal,
       "texte_final": vt[-1800:]}
try:
    res["commandes"] = [{"commande": c["commande"], "approbation": c["approbation"], "erreur": c["erreur"]} for c in commandes(PROJETS[a.projet], depuis=t_debut_ms)]
except Exception as e:  # noqa: BLE001
    res["commandes_erreur"] = repr(e)
try:
    res["outils_appeles"], res["reponse_agent"] = resume(PROJETS[a.projet], t_debut_ms)
except Exception as e:  # noqa: BLE001
    res["resume_erreur"] = repr(e)
try:
    ws = os.path.join(os.path.expanduser("~"), ".lmstudio", "apps", "bionic", "projects", PROJETS[a.projet], "workspace")
    res["fichiers_projet"] = sorted(f for f in os.listdir(ws) if not f.startswith(".") and f != "__pycache__")
except Exception as e:  # noqa: BLE001
    res["fichiers_projet_erreur"] = repr(e)
try:
    res["modele_reel"] = modele_reel(PROJETS[a.projet], t_debut_ms)
    print("modèle réel (base de sessions) :", res["modele_reel"], flush=True)
except Exception as e:  # noqa: BLE001
    res["modele_reel_erreur"] = repr(e)
os.makedirs(SORTIE, exist_ok=True)
with open(os.path.join(SORTIE, f"bionic_{a.etiquette}.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print(json.dumps({k: res[k] for k in ("fin", "duree_mesuree_s", "duree_affichee")}, ensure_ascii=False), flush=True)
print(vt[-900:])
