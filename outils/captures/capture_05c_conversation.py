"""Manuel 05 : conversation à plusieurs tours autour d'une image (lecture de tableau, mémoire de conversation, calcul).
Modèle : Gemma 4 E4B, thinking désactivé. Une seule image jointe, trois questions dans la même conversation."""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from lmcdp import LM

D = "lmstudio/05-vision/"
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
IMG = os.path.join(ROOT, "outils", "resultats", "facture_test_1288.png")
Q = [
    "Quelle est la ligne la plus chère de ce tableau ? Donne sa désignation et son montant total HT.",
    "Quelle part du total HT de la facture cette ligne représente-t-elle, en pourcentage ?",
    "Si le client commandait 2 de ces formations au lieu d'une, quel serait le nouveau total TTC ?",
]

lm = LM(width=1440, height=1500)
lm.close_dialogs(); lm.wait(0.5)


def switch_state():
    return lm.ev("(() => { const s=[...document.querySelectorAll('button[role=switch]')].filter(b=>b.getBoundingClientRect().x>1150)[0]; return s ? s.getAttribute('aria-checked') === 'true' : null })()")


def reponse_terminee(msg):
    """Vrai si « Stop reason » apparaît après la dernière occurrence de la question (la liste des messages est virtualisée :
    compter les occurrences dans la page entière est trompeur)."""
    t = lm.ev("document.body.innerText")
    i = t.rfind(msg[:40])
    return i >= 0 and "Stop reason" in t[i:]


def send(msg, timeout=900):
    lm.click_xy(700, lm.ev("innerHeight") - 85); lm.wait(0.6)
    lm.type(msg); lm.wait(0.8); lm.key("Enter")
    t0 = time.time()
    while time.time() - t0 < timeout:
        time.sleep(1.5)
        if reponse_terminee(msg):
            break
    lm.wait(1.5)
    return round(time.time() - t0, 1)


# charger le modèle (sélecteur Ctrl+L) si nécessaire ; la fenêtre de paramètres s'ouvre : valeurs par défaut, bouton « Load Model »
if "Select a model to load" in lm.visible_text():
    lm.click_xy(21, 90); lm.wait(1.0)
    lm.send("Input.dispatchKeyEvent", type="keyDown", key="l", code="KeyL", modifiers=2, windowsVirtualKeyCode=76)
    lm.send("Input.dispatchKeyEvent", type="keyUp", key="l", code="KeyL", modifiers=2, windowsVirtualKeyCode=76)
    lm.wait(1.5)
    r = lm.rect(text="Gemma 4 E4B")
    lm.click_xy(r[0] + r[2] / 2, r[1] + r[3] / 2); lm.wait(3)
    if lm.has_dialog():
        lm.click_xy(1006, 787)   # bouton « Load Model » de la fenêtre (viewport 1440 x 900)
for _ in range(60):
    if "google/gemma-4-e4b" in lm.visible_text() and "Select a model to load" not in lm.visible_text():
        break
    time.sleep(2)
lm.wait(2)

lm.click_xy(262, 88); lm.wait(7)   # nouvelle conversation
if switch_state():
    lm.click_xy(1414, 548); lm.wait(0.8)
lm.drop_files([IMG], x=700, y=500); lm.wait(1.5)
durees = []
for i, q in enumerate(Q):
    durees.append(send(q))
    if i == 0:
        lm.wait(1)
lm.shot(D + "06-conversation-image-suivi")
txt = lm.ev("document.body.innerText")
json.dump({"durees_s": durees, "texte": txt}, open(os.path.join(ROOT, "outils", "resultats", "e9_conversation_image.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("durées :", durees)
if not switch_state():
    lm.click_xy(1414, 548); lm.wait(0.8)
r = lm.rect(text="Discard unsaved")
if r:
    lm.click_xy(r[0] + r[2] / 2, r[1] + r[3] / 2); lm.wait(1)
print("terminé")
