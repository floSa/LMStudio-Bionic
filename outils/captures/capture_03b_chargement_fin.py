"""Captures 07-09 du Manuel 03 (chargement en cours, modèle chargé, sélecteur). À lancer APRÈS un rechargement de l'interface
(les changements de taille de fenêtre émulée peuvent bloquer le rendu du panneau de chat)."""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lmcdp import LM

D = "lmstudio/03-chargement/"
lm = LM(width=1440, height=900)
lm.close_dialogs(); lm.wait(0.5)
lm.click_xy(21, 90); lm.wait(1.5)

# éjecter puis recharger avec les réglages mémorisés (fenêtre de chargement -> Load Model)
lm.click_xy(926, 48); lm.wait(4)
lm.send("Input.dispatchKeyEvent", type="keyDown", key="l", code="KeyL", modifiers=2, windowsVirtualKeyCode=76)
lm.send("Input.dispatchKeyEvent", type="keyUp", key="l", code="KeyL", modifiers=2, windowsVirtualKeyCode=76)
lm.wait(1.5)
r = lm.rect(selector="[role=dialog] *", text="Gemma 4 E4B")
lm.click_xy(r[0] + 20, r[1] + r[3] / 2); lm.wait(2)
lm.click(selector="[role=dialog] button", text="Load Model")
lm.wait(4)
lm.shot(D + "07-chargement-en-cours")
t0 = time.time()
while time.time() - t0 < 120:
    time.sleep(2)
    if "Eject" in lm.ev("document.body.innerText"):
        break
    if lm.ev("!!document.querySelector('[class*=progress], [role=progressbar]')") is False and time.time() - t0 > 20:
        break
lm.wait(6)
lm.shot(D + "08-modele-charge", annotations=[(527, 35, 380, 28, "1"), (911, 35, 30, 28, "2"), (1016, 846, 48, 28, "3")])
lm.send("Input.dispatchKeyEvent", type="keyDown", key="l", code="KeyL", modifiers=2, windowsVirtualKeyCode=76)
lm.send("Input.dispatchKeyEvent", type="keyUp", key="l", code="KeyL", modifiers=2, windowsVirtualKeyCode=76)
lm.wait(1.5)
lm.shot(D + "09-selecteur-modele-charge")
lm.close_dialogs()
print("ok")
