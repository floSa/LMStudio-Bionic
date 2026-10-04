"""Captures 03/04 du Manuel 04 : même question avec thinking désactivé puis activé (conversation neuve)."""
import os, re, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lmcdp import LM

D = "lmstudio/04-chat/"
lm = LM(width=1440, height=900)
Q = "Combien font 17 x 23 ? Explique brièvement."


def switch_state():
    return lm.ev("(() => { const s=[...document.querySelectorAll('button[role=switch]')].filter(b=>b.getBoundingClientRect().x>1150)[0]; return s ? s.getAttribute('aria-checked') === 'true' : null })()")


def set_thinking(on):
    cur = switch_state()
    if cur is None:
        raise RuntimeError("interrupteur introuvable")
    if cur != on:
        lm.click_xy(1414, 548); lm.wait(0.8)
    assert switch_state() == on


def generating():
    return lm.ev("!!document.querySelector('button[aria-label*=Stop], button[aria-label*=stop]')") or \
        lm.ev("(() => { const r=document.body.innerText; return !r.includes('Stop reason') })()")


def send(msg, timeout=400):
    lm.click_xy(700, 815); lm.wait(0.4)
    lm.type(msg); lm.wait(0.4); lm.key("Enter")
    t0 = time.time(); seen_zero = False
    while time.time() - t0 < timeout:
        time.sleep(1.0)
        c = lm.ev("document.body.innerText").count("Stop reason")
        if c == 0:
            seen_zero = True
        if seen_zero and c >= 1:
            break
    lm.wait(1.5)
    return time.time() - t0


lm.close_dialogs()
lm.click_xy(262, 88); lm.wait(2.5)             # conversation neuve
set_thinking(False)
t_off = send(Q)
lm.shot(D + "04-thinking-desactive")
set_thinking(True)
t_on = send(Q)
lm.shot(D + "03-thinking-actif")
print("durées totales (s) OFF / ON :", round(t_off, 1), round(t_on, 1))
r = lm.rect(text="Discard unsaved")
if r:
    lm.click_xy(r[0] + r[2] / 2, r[1] + r[3] / 2); lm.wait(1)
