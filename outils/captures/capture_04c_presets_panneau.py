"""Captures du Manuel 04 (suite) : presets (création puis suppression du preset d'exemple), panneau de paramètres, menus."""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lmcdp import LM

D = "lmstudio/04-chat/"
lm = LM(width=1440, height=900)
lm.close_dialogs(); lm.wait(0.5)


def text():
    return lm.ev("document.body.innerText")


def delete_current_preset():
    lm.click_xy(1411, 240); lm.wait(1)
    r = lm.rect(text="Delete...", exact=False) or lm.rect(text="Delete…", exact=False)
    if r:
        lm.click_xy(r[0] + 40, r[1] + r[3] / 2); lm.wait(1.2)
        lm.shot(D + "10-preset-suppression")
        # bouton de confirmation dans la boîte de dialogue
        c = lm.ev("""(() => { const d=document.querySelector('[role=dialog]'); if(!d) return null;
          const b=[...d.querySelectorAll('button')].filter(x=>/^delete/i.test((x.innerText||'').trim()))[0]; if(!b) return null;
          const r=b.getBoundingClientRect(); return [r.x+r.width/2, r.y+r.height/2]; })()""")
        if c:
            lm.click_xy(*c); lm.wait(1.5)
        else:
            lm.key("Escape")


# 0. si le preset d'exemple existe déjà, le supprimer pour repartir proprement
if "exemple-extraction" in text():
    delete_current_preset()

# a. modification d'un paramètre -> « Unsaved Preset »
lm.set_value(1386, 766, 0.2); lm.wait(1)
lm.shot(D + "06-preset-modifie", clip=(1160, 140, 280, 260))
lm.click_xy(1290, 240); lm.wait(1.2)
lm.shot(D + "07-preset-nom", clip=(1160, 140, 280, 260))
lm.type("exemple-extraction"); lm.wait(0.5)
lm.click_xy(1365, 240); lm.wait(1.5)
lm.shot(D + "08-preset-enregistre", clip=(1160, 140, 280, 260))
lm.click_xy(1411, 240); lm.wait(1)
lm.shot(D + "09-preset-menu", clip=(1160, 140, 280, 360))
lm.key("Escape"); lm.wait(0.6)
delete_current_preset()
print("presets restants :", os.listdir(os.path.expanduser(r"~\.lmstudio\config-presets")))

# b. Context Overflow et Limit Response Length
lm.click_xy(1340, 840); lm.wait(0.8)
lm.shot(D + "11-context-overflow", clip=(1160, 700, 280, 200))
lm.key("Escape"); lm.wait(0.5)
lm.click_xy(1309, 821); lm.wait(0.8)
lm.shot(D + "12-limite-reponse", clip=(1160, 700, 280, 200))
lm.click_xy(1309, 821); lm.wait(0.6)

# c. menu d'une conversation
lm.click_xy(255, 187); lm.wait(1)
lm.shot(D + "13-menu-conversation", clip=(40, 140, 400, 300))
lm.key("Escape"); lm.wait(0.5)

# d. onglet Integrations du panneau de droite
lm.click_xy(1237, 94); lm.wait(1.2)
lm.shot(D + "14-panneau-integrations", clip=(1160, 68, 280, 400))
lm.click_xy(1356, 94); lm.wait(1)

# e. panneau complet (viewport haut), puis rechargement pour retrouver un affichage sain
lm.viewport(1440, 1500); lm.wait(1.5)
lm.shot(D + "15-panneau-complet", clip=(1160, 68, 280, 1400))
lm.send("Page.reload"); time.sleep(7)
lm = LM(width=1440, height=900)
print("terminé")
