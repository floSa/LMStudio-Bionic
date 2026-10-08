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


def maximiser_fenetre():
    """Met la fenêtre de Bionic en plein écran (Windows) avant toute capture : une fenêtre à moitié ouverte fausse les captures."""
    import subprocess
    cmd = ("Add-Type -Name W -Namespace N -MemberDefinition '[DllImport(\"user32.dll\")] public static extern bool ShowWindow(IntPtr h,int c);';"
           "$p=Get-Process Bionic|Where-Object{$_.MainWindowHandle -ne 0}|Select-Object -First 1;if($p){[N.W]::ShowWindow($p.MainWindowHandle,3)|Out-Null}")
    try:
        subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, timeout=20)
    except Exception:  # noqa: BLE001
        pass


def connect(width=1440, height=900):
    import atexit
    maximiser_fenetre()
    time.sleep(1.5)  # la fenêtre se redimensionne après la mise en plein écran ; attendre avant de fixer la taille émulée
    lm = LM(port=9223, width=width, height=height)
    time.sleep(0.8)

    def _rendre_la_fenetre():
        """Lève l'émulation de taille (1440 × 900) en fin de script : sinon la page n'occupe qu'une partie de la fenêtre maximisée."""
        try:
            lm.send("Emulation.clearDeviceMetricsOverride")
        except Exception:  # noqa: BLE001
            pass
    atexit.register(_rendre_la_fenetre)
    return lm


def visible_at(lm, text, below_y=2000, exact=False):
    """Centre (x, y) du dernier élément réellement visible dont le texte correspond, au-dessus de below_y ; None sinon."""
    js = r"""((t,by,ex)=>{const out=[];for(const e of document.querySelectorAll('body *')){if(e.children.length>0)continue;
      const s=(e.innerText||'').trim();if(!(ex? s===t : s.includes(t)))continue;const r=e.getBoundingClientRect();
      if(r.width===0||r.y>=by)continue;const el=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
      if(el&&(e===el||e.contains(el)||el.contains(e)))out.push([r.x+r.width/2,r.y+r.height/2]);}return out})(%s,%d,%s)""" % (
        json.dumps(text), below_y, "true" if exact else "false")
    o = lm.ev(js)
    return o[-1] if o else None


COLX = None  # centre horizontal de la colonne de la session créée en dernier (l'écran peut être scindé en deux colonnes)


def colonne_vide(lm):
    """Centre horizontal de la zone de saisie vide « Confiez une tâche à Bionic » d'une session neuve (centrée à l'écran, y < 700 ; dans une session en cours elle est en bas)
    et réellement visible (None si absente)."""
    return lm.ev(r"""(()=>{for(const e of document.querySelectorAll('body *')){if(e.children.length>0)continue;
      if(!/^Confiez une tâche à Bionic$/.test((e.innerText||'').trim()))continue;const r=e.getBoundingClientRect();if(r.width===0||r.y>700)continue;
      const el=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);if(!(el&&e.parentElement&&e.parentElement.contains(el)))continue;return r.x+r.width/2}return null})()""")


def new_session(lm, project="Démo code"):
    """Ouvre une nouvelle session vide dans le projet donné et mémorise sa colonne (COLX)."""
    global COLX
    pr = visible_at(lm, "Revenir à l’application", 200)  # les Réglages occupent toute la fenêtre : en sortir d'abord
    if pr:
        lm.click_xy(*pr); lm.wait(2)
    b = lm.ev("(()=>{const e=document.querySelector('[aria-label=\"Créer une session dans " + project + "\"]');if(!e)return null;"
              "const r=e.getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
    if not b:
        raise LookupError("bouton de création de session introuvable pour " + project)
    lm.click_xy(b[0] + b[2] / 2, b[1] + b[3] / 2)
    lm.wait(2)
    for _ in range(8):  # le champ vide se place au centre de la colonne après une courte animation
        COLX = colonne_vide(lm)
        if COLX is not None:
            break
        lm.wait(1)
    if COLX is None:
        raise LookupError("zone de saisie vide de la nouvelle session introuvable")


def model_chip(lm):
    """Bouton du sélecteur de modèle réellement visible : (texte, x, y) ou None.
    Reconnaît « Choisir un modèle » et tout « <modèle> <niveau de raisonnement> » (Activé, Désactivé, Moyen…). Si l'écran est scindé en deux colonnes,
    retient la colonne de la session créée en dernier (COLX, fixée par new_session ; constaté : une nouvelle session s'ouvre tantôt à gauche, tantôt à droite, et agir sur l'autre colonne modifie une ancienne session), hors barre latérale. (Version 1.1.7 : le niveau n'est pas toujours « Activé / Désactivé » ; les onglets masqués restent dans le DOM ;
    dans une session vide, la zone de saisie est au centre de l'écran, donc le bouton n'est pas forcément en bas.)"""
    r = lm.ev(r"""(()=>{const out=[];for(const e of document.querySelectorAll('button')){const t=e.innerText.trim().replace(/\s+/g,' ');
      if(!/^(Choisir un modèle|Gemma|Qwen|Olm[oO]CR)/.test(t))continue;const r=e.getBoundingClientRect();if(r.width===0||r.x<220)continue;if(%s!==null&&Math.abs(r.x+r.width/2-%s)>330)continue;
      const el=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);if(!(el&&e.contains(el)))continue;out.push([t,r.x+r.width/2,r.y+r.height/2])}
      out.sort((a,b)=>a[1]-b[1]);return out})()""" % ((("null" if COLX is None else repr(COLX)),) * 2))
    return r[-1] if r else None


def choose_model(lm, model_text, effort=None, tentatives=3):
    """Sélectionne un modèle (texte exact de l'option) puis, si demandé, l'effort de raisonnement ; vérifie le résultat sur le bouton.
    Lève RuntimeError si le modèle demandé n'est pas sélectionné (constaté : sans cette vérification, une session pouvait partir avec le modèle précédent)."""
    for _ in range(tentatives):
        c = model_chip(lm)
        if c is None or not c[0].startswith(model_text):
            if c is None:
                raise LookupError("sélecteur de modèle introuvable")
            lm.click_xy(c[1], c[2]); lm.wait(1.3)
            pt = visible_at(lm, model_text, 900, exact=True)
            if pt:
                lm.click_xy(*pt); lm.wait(1.5)
            lm.key("Escape"); lm.wait(0.6)
            c = model_chip(lm)
        if c is not None and c[0].startswith(model_text):
            break
    else:
        raise RuntimeError(f"modèle non sélectionné : demandé {model_text!r}, affiché {c!r}")
    if effort and not c[0].endswith(effort):
        lm.click_xy(c[1], c[2]); lm.wait(1.2)
        pe = visible_at(lm, "Effort de raisonnement", 900)
        if pe:
            lm.click_xy(*pe); lm.wait(1.0)
            po = visible_at(lm, effort, 900, exact=True)
            if po:
                lm.click_xy(*po); lm.wait(0.8)
        lm.key("Escape"); lm.wait(0.6)
        c = model_chip(lm)
    return c


def bouton_aria(lm, aria):
    """Centre (x, y) du bouton visible portant cet aria-label dans la colonne de la session créée (COLX) ; None sinon. Exemples : « Mode shell », « Modèle »."""
    r = lm.ev("""((a,cx)=>{const out=[];for(const e of document.querySelectorAll('button')){if(e.getAttribute('aria-label')!==a)continue;const r=e.getBoundingClientRect();
      if(r.width===0||r.x<220)continue;if(cx!==null&&Math.abs(r.x+r.width/2-cx)>330)continue;const el=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
      if(el&&e.contains(el))out.push([r.x+r.width/2,r.y+r.height/2])}return out})(%s,%s)""" % (json.dumps(aria), "null" if COLX is None else repr(COLX)))
    return r[-1] if r else None


def composer_click(lm):
    """Clique dans la zone de saisie (le zone de saisie change de place entre une session vide et une session en cours)."""
    p = lm.ev("""(()=>{const c=[...document.querySelectorAll('[contenteditable=\"true\"],textarea')].filter(e=>{const r=e.getBoundingClientRect();
      if(!(r.width>200&&r.height>10&&getComputedStyle(e).visibility!=='hidden'))return false;const el=document.elementFromPoint(r.x+r.width/2,r.y+Math.min(r.height/2,20));return !!el&&(e===el||e.contains(el)||el.contains(e))});if(!c.length)return null;
      const cx=%s;const d=c.filter(e=>{const r=e.getBoundingClientRect();return cx===null||Math.abs(r.x+r.width/2-cx)<330});if(!d.length)return null;d.sort((a,b)=>a.getBoundingClientRect().y-b.getBoundingClientRect().y);const r=d[d.length-1].getBoundingClientRect();return [r.x+r.width/2,r.y+Math.min(r.height/2,20)]})()""" % ("null" if COLX is None else repr(COLX)))
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
