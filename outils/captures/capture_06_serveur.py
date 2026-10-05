"""Captures du Manuel 06 - Serveur local et API (page Developer)."""
import os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from lmcdp import LM

D = "lmstudio/06-serveur/"
lm = LM(width=1440, height=1100)
lm.close_dialogs(); lm.wait(0.5)
lm.click_xy(21, 124); lm.wait(2.5)       # Developer


def label_rect(text):
    return lm.rect(selector="[role=dialog] *, [role=menu] *, [data-radix-popper-content-wrapper] *", text=text, exact=True)


# 1. page Developer annotée (serveur démarré)
lm.shot(D + "01-page-developer-annotee", annotations=[
    (303, 88, 128, 26, "1"), (447, 88, 105, 26, "2"), (564, 88, 82, 26, "3"), (760, 88, 280, 26, "4"),
    (296, 162, 852, 80, "5"), (296, 515, 852, 262, "6"), (296, 800, 852, 296, "7"), (1170, 80, 270, 400, "8"),
    (51, 100, 223, 70, "9")])

# 2. fenêtre « Server Settings »
lm.click_xy(500, 101); lm.wait(1.5)
rows = ["Server Port", "Require Authentication", "Serve on Local Network", "Allow per-request MCPs",
        "Allow calling servers from mcp.json", "Enable CORS", "Just-in-Time Model Loading",
        "Auto unload unused JIT loaded models", "Only Keep Last JIT Loaded Model"]
items = []
for i, lab in enumerate(rows, 1):
    r = lm.rect(text=lab, exact=True)
    if r:
        items.append((r[0] - 4, r[1] - 4, r[2] + 8, r[3] + 8, str(i)))
    else:
        print("introuvable :", lab)
lm.shot(D + "02-server-settings-annotee", annotations=items, clip=(440, 118, 370, 400))
lm.key("Escape"); lm.wait(0.8)

# 3. onglets des endpoints
for tab, name in (("OpenAI-compatible", "03-endpoints-openai"), ("Anthropic-compatible", "04-endpoints-anthropic"), ("LM Studio API", "05-endpoints-lmstudio")):
    r = lm.rect(text=tab, exact=True)
    if r:
        lm.click_xy(r[0] + r[2] / 2, r[1] + r[3] / 2); lm.wait(1)
        lm.shot(D + name, clip=(296, 510, 852, 275))

# 4. documentation intégrée
lm.click_xy(88, 155); lm.wait(2)
lm.shot(D + "06-documentation-integree")
lm.click_xy(124, 123); lm.wait(1.5)       # retour sur Local Server

# 5. panneau de droite : API Usage
lm.shot(D + "07-api-usage", clip=(1160, 68, 280, 580))
print("terminé")
