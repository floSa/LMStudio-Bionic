"""Captures 11 et 12 du Manuel 04 (Context Overflow, Limit Response Length) en affichage haut, puis retour à l'état d'origine."""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lmcdp import LM

D = "lmstudio/04-chat/"
lm = LM(width=1440, height=1500)
lm.close_dialogs(); lm.wait(1)

r = lm.rect(text="Discard unsaved")
if r:                                         # annule l'état laissé par l'essai précédent
    lm.click_xy(r[0] + r[2] / 2, r[1] + r[3] / 2); lm.wait(1.2)

# Limit Response Length : cocher, capturer, décocher
box = lm.ev("""(() => { const l=[...document.querySelectorAll('*')].filter(e=>e.children.length===0 && (e.textContent||'').trim().startsWith('Limit Response Length'))[0];
  let p=l.parentElement; for(let i=0;i<4;i++){ const b=p.querySelector('button[role=checkbox]'); if(b){const r=b.getBoundingClientRect(); return [r.x+r.width/2,r.y+r.height/2];} p=p.parentElement;} return null })()""")
print("case Limit Response Length :", box)
lm.click_xy(*box); lm.wait(1)
ro = lm.rect(text="Context Overflow", exact=True)
lm.shot(D + "12-limite-reponse", clip=(1160, ro[1] - 110, 280, 190))
lm.click_xy(*box); lm.wait(1)

# Context Overflow : ouvrir la liste
ro = lm.rect(text="Context Overflow", exact=True)
dd = lm.rect(selector="button[role=combobox]", text="Truncate Middle")
lm.click_xy(dd[0] + dd[2] / 2, dd[1] + dd[3] / 2); lm.wait(1)
lm.shot(D + "11-context-overflow", clip=(1160, ro[1] - 60, 280, 190))
lm.key("Escape"); lm.wait(0.6)

r = lm.rect(text="Discard unsaved")
if r:
    lm.click_xy(r[0] + r[2] / 2, r[1] + r[3] / 2); lm.wait(1)
lm.send("Page.reload"); time.sleep(7)
lm = LM(width=1440, height=900)
print("terminé", lm.rect(text="Discard unsaved"))
