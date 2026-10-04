"""Captures du Manuel 04 - Chat et paramètres d'inférence (partie 1 : conversation, statistiques, thinking, éditeur de prompt système).
Usage : python capture_04_chat.py [conversation|thinking|editeur]  (sans argument : tout)"""
import json, os, re, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lmcdp import LM

D = "lmstudio/04-chat/"
which = sys.argv[1:] or ["conversation", "thinking", "editeur"]
lm = LM(width=1440, height=900)   # pas de rechargement de page : après un reload, l'envoi de messages échoue de façon intermittente
lm.wait(1)
lm.close_dialogs()
lm.click_xy(21, 90); lm.wait(1.5)


def stats_count():
    return lm.ev("document.body.innerText").count("Stop reason")


def send(msg, timeout=300):
    """Envoie un message et attend la fin de génération (les statistiques disparaissent au début puis réapparaissent à la fin)."""
    lm.click_xy(700, 815); lm.wait(1.0)
    lm.type(msg); lm.wait(0.8); lm.key("Enter")
    t0 = time.time(); seen_zero = False; clicked = False
    while time.time() - t0 < timeout:
        time.sleep(1.0)
        c = stats_count()
        if c == 0:
            seen_zero = True
        if not seen_zero and not clicked and time.time() - t0 > 5:
            lm.click_xy(1119, 860); clicked = True      # Enter n'a pas été pris en compte : bouton d'envoi
        if seen_zero and c >= 1:
            break
    lm.wait(1.0)
    return time.time() - t0


def switch_thinking():
    return lm.ev("""(() => { const s=[...document.querySelectorAll('button[role=switch]')].filter(b=>b.getBoundingClientRect().x>1150)[0];
      if(!s) return null; const r=s.getBoundingClientRect(); return [r.x+r.width/2, r.y+r.height/2]; })()""")


def discard_unsaved():
    r = lm.rect(text="Discard unsaved", exact=False)
    if r:
        lm.click_xy(r[0] + r[2] / 2, r[1] + r[3] / 2); lm.wait(1)


if "conversation" in which:
    discard_unsaved()
    lm.click_xy(262, 88); lm.wait(7)           # conversation neuve (délai d'initialisation nécessaire), un seul échange
    send("Explique en trois phrases ce qu'est la quantification d'un modèle de langage (ex. Q4_K_M).")
    st = lm.rect(text="Stop reason", exact=False)            # ligne de statistiques (position variable selon la longueur)
    ys = st[1]
    lm.shot(D + "01-conversation-annotee", annotations=[
        (611, 135, 524, 68, "1"), (323, 232, 130, 18, "2"), (323, 260, 190, 24, "3"), (323, 290, 795, ys - 300, "4"),
        (322, ys - 4, 412, 24, "5", "r"), (321, ys + 24, 170, 26, "6", "r"), (1016, 846, 48, 28, "7")])
    lm.click_xy(426, 271); lm.wait(1.2)
    lm.shot(D + "02-bloc-reflexion-deplie")
    lm.click_xy(426, 271); lm.wait(0.8)

if "thinking" in which:
    Q = "Combien font 17 x 23 ? Explique brièvement."
    lm.click_xy(262, 88); lm.wait(2)          # nouvelle conversation dédiée
    for _ in range(10):
        sw = switch_thinking()
        if sw:
            break
        lm.wait(1)
    sw = sw or [1414, 548]      # position constatée de l'interrupteur « Enable Thinking »
    print("switch thinking:", sw)
    dt_on = send(Q)
    lm.shot(D + "03-thinking-actif")
    lm.click_xy(*sw); lm.wait(0.8)
    dt_off = send(Q)
    lm.shot(D + "04-thinking-desactive")
    print("durées mesurées par le script (s) ON / OFF :", round(dt_on, 1), round(dt_off, 1))
    lm.click_xy(*sw); lm.wait(0.8)
    discard_unsaved()

if "editeur" in which:
    lm.send("Input.dispatchKeyEvent", type="keyDown", key="e", code="KeyE", modifiers=2, windowsVirtualKeyCode=69)
    lm.send("Input.dispatchKeyEvent", type="keyUp", key="e", code="KeyE", modifiers=2, windowsVirtualKeyCode=69)
    lm.wait(1.5)
    lm.shot(D + "05-editeur-prompt-systeme")
    r = lm.rect(text="Close Editor")
    if r:
        lm.click_xy(r[0] + r[2] / 2, r[1] + r[3] / 2); lm.wait(1)
print("terminé")
