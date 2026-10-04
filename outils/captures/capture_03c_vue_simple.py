"""Capture 02 du Manuel 03 : fenêtre de chargement en vue simple (sans « Show advanced settings »)."""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
exec(open(os.path.join(HERE, "..", "mesures_estimation_gui.py"), encoding="utf-8").read().split("res = {}")[0])

lm.close_dialogs(); lm.wait(1)
open_loader()
c = controls("Show advanced settings")
print("controles du libellé :", c)
sw = ev = lm.ev("""(() => { const d=document.querySelector('[role=dialog]');
  const leaf=[...d.querySelectorAll('*')].filter(e=>e.children.length===0 && (e.textContent||'').trim()==='Show advanced settings')[0];
  const lr=leaf.getBoundingClientRect(); const bs=[...d.querySelectorAll('button')].filter(b=>{const r=b.getBoundingClientRect(); return Math.abs((r.y+r.height/2)-(lr.y+lr.height/2))<14 && r.x<lr.x});
  return bs.map(b=>{const r=b.getBoundingClientRect(); return [r.x+r.width/2, r.y+r.height/2]}) })()""")
print("interrupteur :", sw)
if "CPU Thread Pool Size" in lm.ev("document.querySelector('[role=dialog]').innerText") and sw:
    lm.click_xy(*sw[0]); lm.wait(1.2)
lm.viewport(1440, 900); lm.wait(1)
lm.shot("lmstudio/03-chargement/02-chargeur-vue-simple", clip=lm.dialog_clip())
print("avancé visible ?", "CPU Thread Pool Size" in lm.ev("document.querySelector('[role=dialog]').innerText"))
# remettre « advanced » pour ne pas modifier la préférence de l'utilisateur
if sw and "CPU Thread Pool Size" not in lm.ev("document.querySelector('[role=dialog]').innerText"):
    lm.click_xy(*sw[0]); lm.wait(1)
lm.click(selector="[role=dialog] button", text="Cancel"); lm.wait(1)
lm.close_dialogs()
