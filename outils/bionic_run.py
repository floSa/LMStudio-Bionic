import time, re, sys, json, os
from lmcdp import LM
MODEL = sys.argv[1]            # texte du modèle à sélectionner
EFFORT = sys.argv[2] if len(sys.argv) > 2 else None   # 'Activé' / 'Désactivé' / None
PROMPT = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] else "Lis la facture jointe et enregistre dans un fichier facture.json : le numéro de facture, la date, le nom du client et le total TTC. Réponds en français."
FILES = [] if (len(sys.argv) > 4 and sys.argv[4] == "-") else sys.argv[4].split(";") if len(sys.argv) > 4 and sys.argv[4] else [os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultats", "facture_test_1288.png")]
TAG = sys.argv[5] if len(sys.argv) > 5 else "run"
PROJECT = os.environ.get('BIONIC_PROJECT', 'Démo documents')
lm = LM(port=9223, width=1440, height=900)
# nouvelle session dans Démo documents
empty = lm.ev("(()=>{const m=[...document.querySelectorAll('[class*=empty],img')];return !![...document.querySelectorAll('div')].find(d=>d.children.length===0&&d.innerText==='Confiez une tâche à Bionic'&&d.getBoundingClientRect().y<600&&d.getBoundingClientRect().y>400)})()")
if True:
    b = lm.ev("(()=>{const e=document.querySelector('[aria-label=\"Créer une session dans " + PROJECT + "\"]');const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
    lm.click_xy(b[0]+b[2]/2, b[1]+b[3]/2); lm.wait(1.5)
print("session vide déjà ouverte:", empty)
chip = lambda: lm.ev(r"(()=>{const bs=[...document.querySelectorAll('button')].filter(e=>/(Activé|Désactivé)\s*$/.test(e.innerText.trim())&&(()=>{const r=e.getBoundingClientRect();const el=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return el&&e.contains(el)})());return bs.map(e=>[e.innerText.trim().replace(/\s+/g,' '),...(()=>{const r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()])})()")
c = chip(); print("chip:", c)
lm.click_xy(c[0][1], c[0][2]); lm.wait(1.2)
def vis(text, below_y, exact=False):
    """Centre d'un élément réellement visible (au-dessus de below_y) dont le texte correspond ; None sinon."""
    js = r"""((t,by,ex)=>{const out=[];for(const e of document.querySelectorAll('body *')){if(e.children.length>0)continue;
      const s=(e.innerText||'').trim();if(!(ex? s===t : s.includes(t)))continue;const r=e.getBoundingClientRect();
      if(r.width===0||r.y>=by)continue;const el=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
      if(el&&(e===el||e.contains(el)||el.contains(e)))out.push([r.x+r.width/2,r.y+r.height/2]);}return out})(%s,%d,%s)""" % (json.dumps(text), below_y, "true" if exact else "false")
    o = lm.ev(js)
    return o[-1] if o else None
cy = c[0][2]
pt = vis(MODEL, cy)
print("option modèle:", pt)
lm.click_xy(pt[0], pt[1]); lm.wait(1.0)
if EFFORT:
    if not vis("Effort de raisonnement", cy):
        lm.click_xy(c[0][1], cy); lm.wait(1.0)
    pe = vis("Effort de raisonnement", cy)
    lm.click_xy(pe[0], pe[1]); lm.wait(1.0)
    po = vis(EFFORT, cy + 40, exact=True)
    print("option effort:", po)
    lm.click_xy(po[0], po[1]); lm.wait(0.8)
lm.key("Escape"); lm.wait(0.6)
print("chip final:", chip())
if FILES:
    lm.drop_files(FILES, x=670, y=500); lm.wait(1.5)
lm.click_xy(700, 487); lm.wait(0.5)
lm.type(PROMPT); lm.wait(0.5)
n0 = lm.text().count("Bionic a terminé sa réponse")
t0 = time.time()
lm.key("Enter")
print("envoyé")
while time.time() - t0 < 1500:
    time.sleep(5)
    t = lm.text()
    if "Action requise" in t:
        print("action requise !"); break
    if t.count("Bionic a terminé sa réponse") > n0:
        break
dur = round(time.time() - t0)
print("durée mesurée (s):", dur)
lm.wait(1)
lm.shot("_b_" + TAG)
vt = lm.visible_text()
i = vt.find("Travail effectué")
print(vt[i-200:i+1500] if i>=0 else vt[-1500:])
