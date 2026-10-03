"""Captures du Manuel 01 - Prise en main de LM Studio. Rejouable : python capture_01_prise_en_main.py"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lmcdp import LM

D = "lmstudio/01-prise-en-main/"
lm = LM(width=1440, height=900)
lm.close_dialogs()
lm.click_xy(21, 90)  # Chat
lm.wait(1.5)


def set_dev_mode(on):
    clip = lm.open_settings("Developer")
    lm.click(selector="[role=dialog] button", text="ON" if on else "OFF", exact=True)
    lm.wait(1)
    return clip


# ---- 1. Anatomie de l'interface (chat ouvert, panneau de droite visible)
items = [
    (7, 76, 28, 140, "1"),                                   # barre de navigation (4 icônes)
    (51, 76, 224, 130, "2"),                                 # liste des conversations
    (527, 35, 380, 28, "3"),                                 # sélecteur de modèle
    (283, 68, 310, 28, "4"),                                 # onglets
    (299, 791, 780, 94, "5"),                                # zone de saisie
]
r = lm.rect(text="Model Parameters")
if r:
    items.append((r[0] - 10, r[1] - 10, 280, 150, "6"))      # panneau paramètres
items += [(1372, 36, 26, 26, "7"), (1404, 36, 26, 26, "8"), (7, 824, 28, 62, "9")]
lm.shot(D + "01-interface-annotee", annotations=items)

# ---- 2. Réglages : toutes les pages
sections = [("General", "02-reglages-general"), ("Appearance", "03-reglages-apparence"),
            ("Chat", "05-reglages-chat"), ("Model Defaults", "06-reglages-model-defaults"), ("Integrations", "07-reglages-integrations"),
            ("LM Link", "08-reglages-lm-link"), ("Runtime", "09-reglages-runtime"), ("Hardware", "10-reglages-hardware")]
for sec, name in sections:
    lm.open_settings(sec)
    lm.wait(0.8)
    print(sec, lm.shot_dialog(D + name), flush=True)

# ---- 3. Mode Developer : OFF puis ON
clip = set_dev_mode(False)
lm.shot(D + "04-reglages-developer-off", clip=clip)
lm.close_dialogs()
lm.viewport(1440, 1500)
lm.wait(1)
lm.shot(D + "11-panneau-parametres-mode-off", clip=(1160, 68, 280, 900))
lm.viewport(1440, 900)
clip = set_dev_mode(True)
lm.shot(D + "04b-reglages-developer-on", clip=clip)
lm.close_dialogs()
lm.viewport(1440, 1500)
lm.wait(1)
lm.shot(D + "12-panneau-parametres-mode-on", clip=(1160, 68, 280, 1400))
lm.viewport(1440, 900)
print("terminé")
