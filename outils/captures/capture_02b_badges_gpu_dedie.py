"""Manuel 02, section 6 : relevé des indicateurs d'adéquation matérielle sur une machine à GPU dédié (RTX 4060 Ti, 16 Go de VRAM, 61,6 Go de RAM)
et capture de la figure 5. LECTURE SEULE : le bouton « Download » n'est jamais ciblé (chaque clic est contrôlé).

Sorties :
  - docs/img/lmstudio/02-modeles/13-badges-adequation.png (figure 5, quatre états)
  - outils/resultats/gpu_badges_telechargement.json (relevé de toutes les lignes lues)
Usage : LM Studio lancé avec le port de debug (outils/lancer_lmstudio_debug.ps1), puis :
  python captures/capture_02b_badges_gpu_dedie.py
"""
import io
import json
import os
import re
import sys

from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lmcdp import LM, DOCS_IMG  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resultats")
lm = LM(width=1440, height=900)

ROWS_JS = r"""[...document.querySelectorAll('[role=option]')].map(o => (o.innerText || '').split(String.fromCharCode(10)).join(' | '))"""
TRIGGER_JS = r"""(() => { const h=[...document.querySelectorAll('div,h1,h2,h3,span')].find(e=>e.children.length===0 && (e.textContent||'').trim()==='Download Options'); if(!h) return null;
  let p=h.parentElement; for(let i=0;i<4&&p;i++){ const c=[...p.querySelectorAll('[role=combobox],button[aria-haspopup],button')].filter(b=>/GB/.test(b.innerText||'') && !/Download\s/.test(b.innerText||''));
    if(c.length){const r=c[0].getBoundingClientRect(); return [r.x+r.width/2-150, r.y+r.height/2, r.y];} p=p.parentElement; } return null; })()"""
CARDS_JS = r"""(() => { const L=document.querySelector('[role=dialog]'); const out=[];
  [...L.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect();return r.x<620 && r.width>300 && r.width<420 && r.height>50 && r.height<80 && e.children.length>0 && (e.innerText||'').length>10})
    .forEach(e=>{const r=e.getBoundingClientRect(); out.push([Math.round(r.y+r.height/2), (e.innerText||'').split(String.fromCharCode(10)).join(' | ').slice(0,90)])});
  const seen=new Set(); return out.filter(o=>{if(seen.has(o[0])) return false; seen.add(o[0]); return true;}); })()"""


def ouvrir_recherche(terme):
    lm.close_dialogs(); lm.wait(1)
    if not lm.has_dialog():
        lm.click_xy(21, 192); lm.wait(3)
    lm.click_xy(420, 143)
    lm.send("Input.dispatchKeyEvent", type="keyDown", key="a", code="KeyA", modifiers=2, commands=["selectAll"])
    lm.send("Input.dispatchKeyEvent", type="keyUp", key="a", code="KeyA", modifiers=2)
    lm.type(terme); lm.wait(7)


def choisir_depot(proprietaire, contient):
    """Attend (jusqu'à 30 s) qu'une carte de résultat du propriétaire voulu apparaisse, puis la sélectionne."""
    for _ in range(15):
        for y, txt in lm.ev(CARDS_JS):
            if proprietaire.lower() in txt.lower() and contient.lower() in txt.lower() and not re.search(r"uncensored|abliterat|heretic", txt, re.I):
                lm.click_xy(420, y); lm.wait(4)
                return txt
        lm.wait(2)
    raise LookupError(f"dépôt introuvable : {proprietaire} / {contient}")


def ouvrir_liste():
    t = lm.ev(TRIGGER_JS)
    lm.click_xy(t[0], t[1]); lm.wait(2)
    return t


def selectionner(quant, taille):
    """Clique la ligne `quant` / `taille` de la liste ouverte (jamais un bouton Download)."""
    rows = lm.ev(ROWS_JS)
    idx = next(i for i, r in enumerate(rows) if f" | {quant} | " in r + " | " and r.endswith(taille + " GB"))
    pos = lm.ev("""((i) => { const o=[...document.querySelectorAll('[role=option]')][i]; o.scrollIntoView({block:'center'}); const r=o.getBoundingClientRect();
        return [r.x+r.width/2-80, r.y+r.height/2, (o.innerText||'')]; })(%d)""" % idx)
    assert "Download" not in pos[2]
    lm.click_xy(pos[0], pos[1]); lm.wait(1.2)


def lire_badge():
    """Texte de l'indicateur affiché sous la liste (le premier motif trouvé dans la zone « Download Options »)."""
    t = lm.ev("(document.querySelector('[role=dialog]').innerText || '')")
    i = t.find("Download Options")
    m = re.search(r"(Full GPU Offload Possible|Partial GPU Offload Possible|Likely too large)", t[i:])
    return m.group(1) if m else "indicateur non lu"


def panneau(path_png):
    t = lm.ev(TRIGGER_JS)
    clip = (634, t[2] - 14, 581, 108)
    data = lm.send("Page.captureScreenshot", format="png", clip=dict(x=clip[0], y=clip[1], width=clip[2], height=clip[3], scale=1))["data"]
    import base64
    return Image.open(io.BytesIO(base64.b64decode(data))).convert("RGB")


panneaux, releves = [], {}
CAS = [  # (terme de recherche, propriétaire du dépôt, fragment du nom, quantification, taille, clé)
    ("mistral small 24b", "unsloth", "GGUF", "IQ4_XS", "14.54", "mistral_small_iq4_xs"),
    ("mistral small 24b", "unsloth", "GGUF", "IQ4_NL", "15.22", "mistral_small_iq4_nl"),
    ("glm 4.5 air", "unsloth", "GGUF", "Q3_K_M", "57.20", "glm45air_q3_k_m"),
    ("glm 4.5 air", "unsloth", "GGUF", "IQ4_XS", "60.48", "glm45air_iq4_xs"),
]
lm.close_dialogs()
for terme, prop, frag, quant, taille, cle in CAS:
    ouvrir_recherche(terme)
    nom = choisir_depot(prop, frag)
    ouvrir_liste()
    rows = lm.ev(ROWS_JS)
    releves[cle] = {"depot": nom, "lignes": rows}
    selectionner(quant, taille)
    releves[cle]["badge_affiche"] = lire_badge()
    print(cle, "->", releves[cle]["badge_affiche"][:160], flush=True)
    panneaux.append(panneau(None))
    lm.close_dialogs(); lm.wait(1.5)

W = max(p.width for p in panneaux)
H = sum(p.height for p in panneaux) + 6 * (len(panneaux) - 1)
fig = Image.new("RGB", (W, H), "white")
y = 0
for p in panneaux:
    fig.paste(p, (0, y)); y += p.height + 6
fig.save(os.path.join(DOCS_IMG, "lmstudio", "02-modeles", "13-badges-adequation.png"))
json.dump(releves, open(os.path.join(OUT, "gpu_badges_telechargement.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
lm.close_dialogs()
print("figure enregistrée")
