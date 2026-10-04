"""Captures du Manuel 03 - Charger un modèle. Charge réellement Gemma 4 E4B (contexte 8192, offload max) à la fin."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
# réutilise les helpers (controls, set_num, open_loader, est...) du script de mesure
exec(open(os.path.join(HERE, "..", "mesures_estimation_gui.py"), encoding="utf-8").read().split("res = {}")[0])

D = "lmstudio/03-chargement/"
lm.viewport(1440, 900)
lm.close_dialogs(); lm.wait(0.8)
lm.click_xy(21, 90); lm.wait(1.5)   # Chat

# 0. décharger le modèle s'il y en a un (bouton d'éjection à droite du sélecteur)
if "google/gemma-4-e4b" in lm.ev("document.body.innerText.slice(0,200)"):
    lm.click_xy(926, 48); lm.wait(4)


def open_picker():
    lm.send("Input.dispatchKeyEvent", type="keyDown", key="l", code="KeyL", modifiers=2, windowsVirtualKeyCode=76)
    lm.send("Input.dispatchKeyEvent", type="keyUp", key="l", code="KeyL", modifiers=2, windowsVirtualKeyCode=76)
    lm.wait(1.5)


def adv_state():
    return "CPU Thread Pool Size" in lm.ev("document.querySelector('[role=dialog]').innerText")


def set_adv(on):
    if adv_state() != on:
        r = lm.rect(selector="[role=dialog] *", text="Show advanced settings", exact=True)
        lm.click_xy(r[0] + r[2] / 2, r[1] + r[3] / 2); lm.wait(1)


def head_clip():
    c = lm.dialog_clip()
    return (c[0], c[1], c[2], 215)


# 1. sélecteur sans modèle chargé
open_picker()
lm.shot(D + "01-selecteur-aucun-modele")
r = lm.rect(selector="[role=dialog] *", text="Gemma 4 E4B")
lm.click_xy(r[0] + 20, r[1] + r[3] / 2); lm.wait(2)

# 2. fenêtre de chargement : vue simple puis avancée
lm.viewport(1440, 1500); lm.wait(1)
set_adv(False)
lm.shot(D + "02-chargeur-vue-simple", clip=lm.dialog_clip())
set_adv(True)
labels = ["Context Length", "GPU Offload", "CPU Thread Pool Size", "Evaluation Batch Size", "Physical Batch Size",
          "Max Concurrent Predictions", "Unified KV Cache", "Context Checkpoints", "Reasoning Budget Message",
          "RoPE Frequency Base", "RoPE Frequency Scale", "Offload KV Cache to GPU Memory", "Keep Model in Memory",
          "Try mmap()", "Seed", "Speculative Decoding", "Chat Template", "Flash Attention",
          "K Cache Quantization Type", "V Cache Quantization Type", "llama.cpp Arguments Override"]
items = []
for i, lab in enumerate(labels, 1):
    r = lm.rect(selector="[role=dialog] *", text=lab, exact=True)
    if r:
        items.append((r[0] - 2, r[1] - 3, r[2] + 4, r[3] + 6, str(i), "r"))
    else:
        print("label introuvable :", lab)
# estimation mémoire
r = lm.rect(selector="[role=dialog] *", text="Estimated Memory Usage", exact=True)
if r:
    items.append((r[0] - 4, r[1] - 6, 740, r[3] + 12, "A"))
lm.shot(D + "03-chargeur-vue-avancee-annotee", annotations=items, clip=lm.dialog_clip())
print("OK 03", len(items))

# 3. effet du contexte sur l'estimation mémoire (en-tête de la fenêtre)
for ctx, name in ((2048, "04a-estimation-contexte-2k"), (131072, "04b-estimation-contexte-128k")):
    set_num("Context Length", ctx); est()
    lm.shot(D + name, clip=head_clip())
set_num("Context Length", 8192); est()

# 4. liste déroulante de quantification du cache K
c = controls("K Cache Quantization Type")
lm.click_xy(c[0][1], c[0][2]); lm.wait(0.8)
c = controls("K Cache Quantization Type")
lm.click_xy(c[-1][1], c[-1][2]); lm.wait(1)
cl = lm.dialog_clip()
lm.shot(D + "05-quantification-cache-k", clip=(cl[0], c[0][2] - 220, cl[2], 330))
lm.key("Escape"); lm.wait(0.5)
if not lm.has_dialog():            # Escape a fermé toute la fenêtre : on la rouvre
    open_loader()
c = controls("K Cache Quantization Type")
if len(c) > 1 or "F16" in lm.ev("document.querySelector('[role=dialog]').innerText.split('K Cache')[1].slice(0,120)"):
    chk = [x for x in c if x[0] == "BUTTON"][0]
    lm.click_xy(chk[1], chk[2]); lm.wait(0.6)

# 5. réglages finaux et chargement réel
set_num("Context Length", 8192); est()
set_num("GPU Offload", 42)
set_num("Max Concurrent Predictions", 4)
lm.shot(D + "06-chargeur-reglages-finaux", clip=head_clip())
lm.click(selector="[role=dialog] button", text="Load Model")
lm.wait(3)
lm.viewport(1440, 900); lm.wait(0.5)
lm.shot(D + "07-chargement-en-cours")
t0 = time.time()
while time.time() - t0 < 120:
    time.sleep(2)
    if "Eject" in lm.ev("document.body.innerText") or "google/gemma-4-e4b" in lm.ev("document.body.innerText.slice(0,160)"):
        break
lm.wait(2)
lm.shot(D + "08-modele-charge")
open_picker()
lm.shot(D + "09-selecteur-modele-charge")
lm.close_dialogs()
print("terminé")
