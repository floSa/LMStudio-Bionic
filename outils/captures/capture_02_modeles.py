"""Captures du Manuel 02 - Modèles. AUCUN téléchargement : le bouton Download n'est jamais cliqué."""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lmcdp import LM

D = "lmstudio/02-modeles/"
lm = LM(width=1440, height=900)
lm.close_dialogs(); lm.wait(0.8)

# ---- 1. My Models
lm.click_xy(21, 158); lm.wait(2)
lm.click_xy(600, 179); lm.wait(1)   # sélectionner la ligne du modèle
lm.shot(D + "01-my-models-annotee", annotations=[
    (51, 100, 223, 160, "1"),       # catégories
    (283, 118, 812, 86, "2"),       # tableau
    (788, 80, 300, 24, "3"),        # filtre
    (950, 163, 125, 32, "4"),       # actions
    (1110, 154, 316, 34, "5", "r"),  # onglets Info / Load / Inference
    (1110, 112, 316, 34, "6"),       # use in new chat / load
    (300, 862, 790, 26, "7"),       # pied de page
])
lm.viewport(1440, 1400); lm.wait(1)
lm.click_xy(1166, 171); lm.wait(1)
lm.shot(D + "02-my-models-info", clip=(1096, 68, 344, 520))
lm.click_xy(1260, 171); lm.wait(1.2)
lm.shot(D + "03-my-models-load", clip=(1096, 68, 344, 1330))
lm.click_xy(1372, 171); lm.wait(1.2)
lm.shot(D + "04-my-models-inference", clip=(1096, 68, 344, 1330))
lm.click_xy(1166, 171)
lm.viewport(1440, 900); lm.wait(1)

# ---- 2. Model Search (modale) - lecture seule
lm.click_xy(21, 192); lm.wait(3)
lm.shot(D + "05-model-search-staff-picks")
dl = None  # le bouton Download n'est jamais ciblé par un clic ; sa position n'est utilisée que pour l'annotation
lm.click_xy(420, 143)
lm.type("gemma 4")
lm.wait(6)
lm.shot(D + "06-model-search-gemma")
# efface et cherche olmocr
lm.click_xy(420, 143)
lm.send("Input.dispatchKeyEvent", type="keyDown", key="a", code="KeyA", modifiers=2, commands=["selectAll"])
lm.send("Input.dispatchKeyEvent", type="keyUp", key="a", code="KeyA", modifiers=2)
lm.type("olmocr")
lm.wait(6)
items = [(224, 125, 380, 36, "1"), (510, 167, 96, 26, "2"), (223, 203, 385, 62, "3"), (645, 270, 560, 90, "4"), (645, 400, 560, 40, "5")]
items.append((1024, 447, 180, 30, "6"))  # bouton Download : repère visuel UNIQUEMENT, ne jamais cliquer
lm.shot(D + "07-model-search-olmocr-annotee", annotations=items)
lm.click_xy(925, 419); lm.wait(1.5)   # liste déroulante des quantifications (pas le bouton Download)
lm.shot(D + "08-model-search-olmocr-quantifications")
lm.key("Escape"); lm.wait(0.5)
lm.close_dialogs(); lm.wait(0.8)

# ---- 3. Téléchargements
lm.click_xy(1386, 49); lm.wait(1.5)
lm.shot(D + "09-panneau-telechargements")
lm.close_dialogs(); lm.key("Escape"); lm.wait(0.5)

# ---- 4. Sélecteur de modèle (Ctrl+L)
lm.click_xy(21, 90); lm.wait(1.5)
lm.send("Input.dispatchKeyEvent", type="keyDown", key="l", code="KeyL", modifiers=2, windowsVirtualKeyCode=76)
lm.send("Input.dispatchKeyEvent", type="keyUp", key="l", code="KeyL", modifiers=2, windowsVirtualKeyCode=76)
lm.wait(1.5)
lm.shot(D + "10-selecteur-modele")
lm.close_dialogs()
print("terminé")
