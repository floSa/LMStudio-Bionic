"""Captures du Manuel 05 - Vision et documents. Images de test fictives générées par outils/experiences_api.py."""
import os, re, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from lmcdp import LM

D = "lmstudio/05-vision/"
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
IMG1288 = os.path.join(ROOT, "outils", "resultats", "facture_test_1288.png")
IMG640 = os.path.join(ROOT, "outils", "resultats", "facture_test_640.png")
DOC = os.path.join(ROOT, "docs", "lmstudio", "annexe-glossaire.md")
PROMPT = "Transcris fidèlement tout le texte de ce document en Markdown (conserve le tableau). Ne rajoute aucun commentaire."

lm = LM(width=1440, height=900)
lm.close_dialogs(); lm.wait(0.5)


def switch_state():
    return lm.ev("(() => { const s=[...document.querySelectorAll('button[role=switch]')].filter(b=>b.getBoundingClientRect().x>1150)[0]; return s ? s.getAttribute('aria-checked') === 'true' : null })()")


def set_thinking(on):
    if switch_state() != on:
        lm.click_xy(1414, 548); lm.wait(0.8)


def send(msg, timeout=600):
    lm.click_xy(700, 815); lm.wait(0.6)
    lm.type(msg); lm.wait(0.8); lm.key("Enter")
    t0 = time.time(); seen_zero = False; clicked = False
    while time.time() - t0 < timeout:
        time.sleep(1.0)
        c = lm.ev("document.body.innerText").count("Stop reason")
        if c == 0:
            seen_zero = True
        if not seen_zero and not clicked and time.time() - t0 > 6:
            lm.click_xy(1119, 860); clicked = True
        if seen_zero and c >= 1:
            break
    lm.wait(1.5)
    return time.time() - t0


def input_y():
    r = lm.rect(text="Send a message to the model", exact=False)
    return r[1] if r else 815


# 1. conversation neuve + image jointe (glisser-déposer)
lm.click_xy(262, 88); lm.wait(7)
set_thinking(False)
lm.drop_files([IMG1288], x=700, y=500); lm.wait(1)
lm.shot(D + "01-image-jointe", annotations=[(307, 718, 66, 66, "1"), (300, 790, 840, 94, "2")])
t1 = send(PROMPT)
lm.shot(D + "02-ocr-1288")
# 2. même document réduit à 640 px
lm.drop_files([IMG640], x=700, y=500); lm.wait(1)
t2 = send(PROMPT)
lm.shot(D + "03-ocr-640")
print("durées (s) 1288 / 640 :", round(t1, 1), round(t2, 1))

# 3. document texte joint
lm.click_xy(262, 88); lm.wait(7)
lm.drop_files([DOC], x=700, y=500); lm.wait(2)
lm.shot(D + "04-document-joint")
t3 = send("Quelle est la définition de TTFT dans ce glossaire ? Réponds en une phrase.")
lm.shot(D + "05-document-reponse")
print("durée document (s) :", round(t3, 1))
set_thinking(True)
r = lm.rect(text="Discard unsaved")
if r:
    lm.click_xy(r[0] + r[2] / 2, r[1] + r[3] / 2); lm.wait(1)
print("terminé")
