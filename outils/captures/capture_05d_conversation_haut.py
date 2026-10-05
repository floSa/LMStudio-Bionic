"""Manuel 05 : capture du haut de la conversation (image, questions 1 et 2) ; la capture 06 existante montre la question 3.
À lancer juste après capture_05c_conversation.py, avec la conversation ouverte."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from lmcdp import LM

D = "lmstudio/05-vision/"
lm = LM(width=1440, height=1500)
os.replace(os.path.join(os.path.dirname(HERE), "..", "docs", "img", "lmstudio", "05-vision", "06-conversation-image-suivi.png"),
           os.path.join(os.path.dirname(HERE), "..", "docs", "img", "lmstudio", "05-vision", "07-conversation-image-calcul.png"))
lm.ev("""(() => { const els=[...document.querySelectorAll('*')].filter(e=>{const r=e.getBoundingClientRect(); return e.scrollHeight>e.clientHeight+50 && r.x>280 && r.x<400 && r.width>600 && getComputedStyle(e).overflowY!=='visible'});
  els.forEach(e=>e.scrollTop=0); return els.length })()""")
lm.wait(1.5)
lm.shot(D + "06-conversation-image-suivi", clip=(284, 68, 800, 1100))
print("ok")
