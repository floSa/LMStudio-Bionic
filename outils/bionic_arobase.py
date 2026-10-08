"""Essai du déclenchement manuel d'une compétence de projet avec `@` (palette) dans une nouvelle session Bionic.

Prérequis : voir bionic_tache.py ; la compétence `compte-rendu-reunion` copiée dans `<dossier du projet>\\.agents\\skills\\` (projet « Démo code »).
Usage : python bionic_arobase.py "Gemma 4 26B A4B" etiquette
Résultat : outils/resultats/gpu_dedie/bionic_<étiquette>.json (modèle réel, durée, réponse)
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bionic_lib import choose_model, composer_click, connect, new_session  # noqa: E402
from lire_approbations_bionic import modele_reel, resume  # noqa: E402

ICI = os.path.dirname(os.path.abspath(__file__))
PROJET = "41716555-c06b-4e4a-9b3c-3be762d6131d"
modele, etiquette = sys.argv[1], sys.argv[2]
NOTES = (" Rédige le compte rendu de cette réunion. Notes : réunion du jeudi 8 octobre ; présents : Alice (cheffe de projet), Marc (technique), Léa (finance) ; "
         "décisions : le lancement est reporté à la semaine suivante, le budget de formation est validé ; action : Marc prépare la démonstration, échéance vendredi ; "
         "question ouverte : qui contacte le fournisseur, personne n'a été désigné.")

lm = connect(1440, 900)
new_session(lm, "Démo code")
t_debut_ms = int(time.time() * 1000)
print("modèle :", choose_model(lm, modele, "Désactivé"), flush=True)
composer_click(lm)
lm.type("@compte"); lm.wait(2)
# entrées de la palette dont le texte contient « compte-rendu » : la première (la plus haute) est la compétence
entrees = lm.ev(r"""(()=>{const out=[];for(const e of document.querySelectorAll('body *')){if(e.children.length>0)continue;const s=(e.innerText||'').trim();
  if(!/compte-rendu/i.test(s)||s.length>60)continue;const r=e.getBoundingClientRect();if(r.width===0)continue;const el=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
  if(el&&(e===el||e.contains(el)||el.contains(e)))out.push([s,r.x+r.width/2,r.y+r.height/2])}out.sort((a,b)=>a[2]-b[2]);return out})()""")
print("entrées de la palette :", entrees, flush=True)
if not entrees:
    raise LookupError("palette @ : aucune entrée « compte-rendu »")
lm.click_xy(entrees[0][1], entrees[0][2]); lm.wait(1)
lm.type(NOTES); lm.wait(0.5)
n0 = lm.text().count("Bionic a terminé sa réponse")
t0 = time.time()
lm.key("Enter")
raison = "délai dépassé"
while time.time() - t0 < 400:
    time.sleep(3)
    t = lm.text()
    if "Votre agent souhaite exécuter des commandes shell" in t or "Action requise" in t:
        raison = "action requise"; break
    if t.count("Bionic a terminé sa réponse") > n0:
        raison = "terminé"; break
duree = round(time.time() - t0)
outils, reponse = resume(PROJET, t_debut_ms)
res = {"etiquette": etiquette, "modele": modele, "modele_reel": modele_reel(PROJET, t_debut_ms), "declenchement": "@ (palette)", "fin": raison,
       "duree_mesuree_s": duree, "outils_appeles": outils, "reponse_agent": reponse}
with open(os.path.join(ICI, "resultats", "gpu_dedie", f"bionic_{etiquette}.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print(json.dumps({k: res[k] for k in ("modele_reel", "fin", "duree_mesuree_s", "outils_appeles")}, ensure_ascii=False))
print(reponse)
