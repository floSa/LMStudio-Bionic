"""Mesure de la compaction (`/compact`) d'une session Bionic : remplit le contexte (lecture d'un long fichier fictif du projet),
puis lance /compact et relève le compteur de contexte avant / après et la durée.

Prérequis : voir bionic_tache.py ; fichier `rapport.txt` (≈ 42 Ko, fictif) dans les fichiers du projet « Démo code ».
Usage : python bionic_compact.py "Gemma 4 E4B" etiquette [consigne]  (consigne facultative : lecture plus courte pour un modèle chargé avec un petit contexte)
Résultat : outils/resultats/gpu_dedie/bionic_compact_<étiquette>.json
"""
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bionic_lib  # noqa: E402
from bionic_lib import choose_model, composer_click, connect, model_chip, new_session, visible_at  # noqa: E402
from lire_approbations_bionic import modeles_sessions  # noqa: E402

ICI = os.path.dirname(os.path.abspath(__file__))
modele, etiquette = sys.argv[1], sys.argv[2]
lm = connect(1440, 900)
new_session(lm, "Démo code")
t_debut_ms = int(time.time() * 1000)
choose_model(lm, modele, "Désactivé")


def contexte():
    """Compteur « Contexte : X k » de la colonne de la session créée (bionic_lib.COLX : l'écran peut être scindé en deux colonnes)."""
    r = lm.ev(r"""(()=>{const out=[];for(const e of document.querySelectorAll('body *')){if(e.children.length>0)continue;const s=(e.innerText||'').replace(/\s+/g,' ').trim();
      const m=s.match(/^Contexte ?: ?([\d,\.]+) ?k$/);if(!m)continue;const r=e.getBoundingClientRect();if(r.width===0)continue;const el=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);if(!(el&&(e===el||e.contains(el)||el.contains(e))))continue;out.push([Math.abs(r.x+r.width/2-%s),m[1]])}
      out.sort((a,b)=>a[0]-b[0]);return out.length?out[0][1]:null})()""" % bionic_lib.COLX)
    return r


def attendre(n0, delai=900):
    t0 = time.time()
    while time.time() - t0 < delai:
        time.sleep(3)
        t = lm.text()
        if "Votre agent souhaite exécuter des commandes shell" in t:
            lm.click_xy(*visible_at(lm, "Vérification automatique (recommandée)", 900)); lm.wait(2)
        if t.count("Bionic a terminé sa réponse") > n0:
            return round(time.time() - t0)
    return None


consigne = sys.argv[3] if len(sys.argv) > 3 else "Lis le fichier rapport.txt en entier (avec l'outil de lecture de fichier) puis donne-moi le code d'archivage figurant à la fin et un résumé en trois points."
composer_click(lm); lm.type(consigne); lm.wait(0.4)
n0 = lm.text().count("Bionic a terminé sa réponse")
lm.key("Enter")
d_lecture = attendre(n0)
lm.wait(2)
avant = contexte()
print("lecture terminée en", d_lecture, "s ; contexte", avant, flush=True)

composer_click(lm); lm.type("/compact"); lm.wait(1.0)
lm.key("Enter"); lm.wait(0.5)
t0 = time.time()
vu_compacting = False
fin = None
while time.time() - t0 < 900:
    time.sleep(2)
    t = lm.text()
    if "Compacting" in t:
        vu_compacting = True
    if vu_compacting and "Compacting" not in t and "Compacted" in t:
        fin = round(time.time() - t0)
        break
    if not vu_compacting and "Compacted" in t and time.time() - t0 > 6:
        fin = round(time.time() - t0)
        break
lm.wait(2)
apres = contexte()
print("compaction :", fin, "s ; contexte", apres, flush=True)
time.sleep(3)
reel = modeles_sessions("41716555-c06b-4e4a-9b3c-3be762d6131d", t_debut_ms)
print("modèles réels (base) :", reel, flush=True)
res = {"modeles_reels": reel, "modele": modele, "lecture_s": d_lecture, "contexte_avant_k": avant, "compaction_s": fin, "contexte_apres_k": apres, "compacting_vu": vu_compacting}
with open(os.path.join(ICI, "resultats", "gpu_dedie", f"bionic_compact_{etiquette}.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
print(res)
