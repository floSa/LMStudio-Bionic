"""Fonctions de pilotage de Bionic (CDP, port 9223) partagées par les scripts de capture et de test du lot 2.

Prérequis : Bionic lancé avec --remote-debugging-port=9223 ; LM Studio fermé (les deux applications ne cohabitent pas).
Les sélecteurs reposent sur les libellés de l'interface française de Bionic 1.1.7.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lmcdp import LM  # noqa: E402


def connect(width=1440, height=900):
    return LM(port=9223, width=width, height=height)


def visible_at(lm, text, below_y=2000, exact=False):
    """Centre (x, y) du dernier élément réellement visible dont le texte correspond, au-dessus de below_y ; None sinon."""
    js = r"""((t,by,ex)=>{const out=[];for(const e of document.querySelectorAll('body *')){if(e.children.length>0)continue;
      const s=(e.innerText||'').trim();if(!(ex? s===t : s.includes(t)))continue;const r=e.getBoundingClientRect();
      if(r.width===0||r.y>=by)continue;const el=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
      if(el&&(e===el||e.contains(el)||el.contains(e)))out.push([r.x+r.width/2,r.y+r.height/2]);}return out})(%s,%d,%s)""" % (
        json.dumps(text), below_y, "true" if exact else "false")
    o = lm.ev(js)
    return o[-1] if o else None


def new_session(lm, project="Démo code"):
    """Ouvre une nouvelle session vide dans le projet donné."""
    b = lm.ev("(()=>{const e=document.querySelector('[aria-label=\"Créer une session dans " + project + "\"]');if(!e)return null;"
              "const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
    if not b:
        raise LookupError("bouton de création de session introuvable pour " + project)
    lm.click_xy(b[0] + b[2] / 2, b[1] + b[3] / 2)
    lm.wait(2)


def model_chip(lm):
    """Bouton du sélecteur de modèle (texte se terminant par Activé ou Désactivé) : (texte, x, y) ou None."""
    r = lm.ev(r"""(()=>{const bs=[...document.querySelectorAll('button')].filter(e=>/(Activé|Désactivé)\s*$/.test(e.innerText.trim())&&(()=>{
      const r=e.getBoundingClientRect();const el=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return el&&e.contains(el)})());
      return bs.map(e=>{const r=e.getBoundingClientRect();return [e.innerText.trim().replace(/\s+/g,' '),r.x+r.width/2,r.y+r.height/2]})})()""")
    return r[0] if r else None


def choose_model(lm, model_text, effort=None):
    """Sélectionne un modèle (texte de l'option) et l'effort de raisonnement ('Activé' / 'Désactivé')."""
    c = model_chip(lm)
    lm.click_xy(c[1], c[2]); lm.wait(1.2)
    cy = c[2]
    pt = visible_at(lm, model_text, cy)
    if pt:
        lm.click_xy(*pt); lm.wait(1.0)
    if effort:
        if not visible_at(lm, "Effort de raisonnement", cy):
            c = model_chip(lm)
            lm.click_xy(c[1], c[2]); lm.wait(1.0)
        pe = visible_at(lm, "Effort de raisonnement", cy)
        lm.click_xy(*pe); lm.wait(1.0)
        po = visible_at(lm, effort, cy + 40, exact=True)
        lm.click_xy(*po); lm.wait(0.8)
    lm.key("Escape"); lm.wait(0.6)
    return model_chip(lm)


def composer_click(lm):
    """Clique dans la zone de saisie (le zone de saisie change de place entre une session vide et une session en cours)."""
    p = lm.ev("""(()=>{const c=[...document.querySelectorAll('[contenteditable=\"true\"],textarea')].filter(e=>{const r=e.getBoundingClientRect();
      return r.width>200&&r.height>10&&getComputedStyle(e).visibility!=='hidden'});if(!c.length)return null;
      const r=c[c.length-1].getBoundingClientRect();return [r.x+r.width/2,r.y+Math.min(r.height/2,20)]})()""")
    if not p:
        raise LookupError("zone de saisie introuvable")
    lm.click_xy(*p)
    lm.wait(0.4)


def send(lm, prompt):
    composer_click(lm)
    lm.type(prompt)
    lm.wait(0.4)
    lm.key("Enter")


def wait_idle(lm, timeout=900, poll=4, stop_on=("Action requise",)):
    """Attend la fin de la réponse (« Bionic a terminé sa réponse ») ou l'un des textes de stop_on. Retourne (raison, secondes)."""
    n0 = lm.text().count("Bionic a terminé sa réponse")
    t0 = time.time()
    while time.time() - t0 < timeout:
        time.sleep(poll)
        t = lm.text()
        for s in stop_on:
            if s in t:
                return s, round(time.time() - t0)
        if t.count("Bionic a terminé sa réponse") > n0:
            return "terminé", round(time.time() - t0)
    return "délai dépassé", round(time.time() - t0)
