"""Pilotage de LM Studio (Electron) via Chrome DevTools Protocol, pour produire les captures des tutoriels.

Prérequis : LM Studio lancé avec --remote-debugging-port=9222 (voir outils/lancer_lmstudio_debug.ps1).
Dépendances : websocket-client, pillow.
"""
import base64
import json
import os
import time
import urllib.request

import websocket

PORT = 9222
DOCS_IMG = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "img"))


class LM:
    def __init__(self, port=PORT, width=1440, height=900):
        pages = None
        for _ in range(10):  # le port de debug est parfois indisponible quelques secondes
            try:
                pages = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json"))
                break
            except OSError:
                time.sleep(2)
        if pages is None:
            raise ConnectionError("LM Studio n'écoute pas sur le port de debug (voir outils/lancer_lmstudio_debug.ps1)")
        page = next(p for p in pages if p["type"] == "page")
        self.ws = websocket.create_connection(page["webSocketDebuggerUrl"], max_size=None, timeout=30, suppress_origin=True)
        self._id = 0
        self.events = []
        self.send("Page.enable")
        self.send("Runtime.enable")
        self.viewport(width, height)

    # --- bas niveau -------------------------------------------------------
    def send(self, method, **params):
        self._id += 1
        mid = self._id
        self.ws.send(json.dumps({"id": mid, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == mid:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})
            if "method" in msg:
                self.events.append(msg)

    def ev(self, expr):
        """Évalue du JS dans la page, retourne la valeur (JSON)."""
        r = self.send("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True)
        if "exceptionDetails" in r:
            raise RuntimeError(r["exceptionDetails"].get("exception", {}).get("description", str(r)))
        return r["result"].get("value")

    def viewport(self, w, h, scale=1):
        self.send("Emulation.setDeviceMetricsOverride", width=w, height=h, deviceScaleFactor=scale, mobile=False)

    # --- interaction ------------------------------------------------------
    def rect(self, selector=None, text=None, nth=0, exact=False):
        """Rectangle (x,y,w,h) d'un élément visible trouvé par sélecteur CSS et/ou texte."""
        js = """((sel, txt, nth, exact) => {
          let els = sel ? [...document.querySelectorAll(sel)] : [...document.querySelectorAll('body *')];
          els = els.filter(e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e);
            return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; });
          if (txt) {
            const t = txt.toLowerCase();
            els = els.filter(e => { const s = (e.innerText || e.getAttribute('aria-label') || e.title || '').trim().toLowerCase(); return exact ? s === t : s.includes(t); });
            // garder le plus profond (le plus spécifique)
            els = els.filter(e => ![...e.children].some(c => els.includes(c)));
          }
          const e = els[nth]; if (!e) return null;
          const r = e.getBoundingClientRect(); return [r.x, r.y, r.width, r.height];
        })(%s, %s, %d, %s)""" % (json.dumps(selector), json.dumps(text), nth, "true" if exact else "false")
        return self.ev(js)

    def click_xy(self, x, y, double=False, clicks=None):
        n = clicks or (2 if double else 1)
        self.send("Input.dispatchMouseEvent", type="mouseMoved", x=x, y=y)
        for i in range(1, n + 1):
            for t in ("mousePressed", "mouseReleased"):
                self.send("Input.dispatchMouseEvent", type=t, x=x, y=y, button="left", clickCount=i)
        time.sleep(0.4)

    def set_value(self, x, y, value):
        """Remplace le contenu d'un champ texte situé en (x,y) puis valide par Tab."""
        self.click_xy(x, y, clicks=3)
        self.send("Input.dispatchKeyEvent", type="keyDown", key="a", code="KeyA", modifiers=2, commands=["selectAll"])
        self.send("Input.dispatchKeyEvent", type="keyUp", key="a", code="KeyA", modifiers=2)
        self.type(str(value))
        self.key("Tab")
        time.sleep(0.5)

    def click(self, selector=None, text=None, nth=0, double=False, exact=False):
        r = self.rect(selector, text, nth, exact)
        if not r:
            raise LookupError(f"introuvable: selector={selector!r} text={text!r}")
        self.click_xy(r[0] + r[2] / 2, r[1] + r[3] / 2, double)

    def hover(self, selector=None, text=None, nth=0):
        r = self.rect(selector, text, nth)
        self.send("Input.dispatchMouseEvent", type="mouseMoved", x=r[0] + r[2] / 2, y=r[1] + r[3] / 2)
        time.sleep(0.5)

    def type(self, s):
        self.send("Input.insertText", text=s)

    def key(self, key, code=None, ctrl=False, shift=False, alt=False):
        mod = (2 if ctrl else 0) | (8 if shift else 0) | (1 if alt else 0)
        vk = {"Enter": 13, "Escape": 27, "Tab": 9, "Backspace": 8}.get(key)
        for t in ("keyDown", "keyUp"):
            p = dict(type=t, key=key, modifiers=mod)
            if code:
                p["code"] = code
            if vk:
                p["windowsVirtualKeyCode"] = vk
            if len(key) == 1 and t == "keyDown" and not ctrl:
                p["text"] = key
            self.send("Input.dispatchKeyEvent", **p)
        time.sleep(0.3)

    def scroll(self, dy, x=700, y=450):
        self.send("Input.dispatchMouseEvent", type="mouseWheel", x=x, y=y, deltaX=0, deltaY=dy)
        time.sleep(0.4)

    def goto(self, hash_route):
        self.ev(f"location.hash = {json.dumps(hash_route)}")
        time.sleep(1)

    def attach_files(self, paths, x=323, y=860):
        """Joint des fichiers au chat : clique sur « + » et répond au sélecteur de fichiers natif à la place de l'utilisateur."""
        self.events.clear()
        self.send("Page.setInterceptFileChooserDialog", enabled=True)
        self.click_xy(x, y)
        for _ in range(30):
            try:
                self.ws.settimeout(0.5)
                msg = json.loads(self.ws.recv())
                if "method" in msg:
                    self.events.append(msg)
            except Exception:
                pass
            finally:
                self.ws.settimeout(30)
            ev = [e for e in self.events if e["method"] == "Page.fileChooserOpened"]
            if ev:
                self.send("DOM.setFileInputFiles", files=list(paths), backendNodeId=ev[0]["params"]["backendNodeId"])
                self.send("Page.setInterceptFileChooserDialog", enabled=False)
                time.sleep(1.5)
                return True
        self.send("Page.setInterceptFileChooserDialog", enabled=False)
        return False

    def drop_files(self, paths, x=700, y=500):
        """Simule le glisser-déposer de fichiers locaux sur la zone (x, y) de la fenêtre."""
        data = {"items": [], "files": list(paths), "dragOperationsMask": 1}
        self.send("Input.setInterceptDrags", enabled=False)
        for t in ("dragEnter", "dragOver", "drop"):
            self.send("Input.dispatchDragEvent", type=t, x=x, y=y, data=data)
            time.sleep(0.3)
        time.sleep(1.5)

    def visible_text(self):
        """Texte des seuls éléments feuilles réellement visibles (ignore les onglets masqués conservés dans le DOM)."""
        return self.ev("""[...document.querySelectorAll('body *')].filter(e=>e.children.length===0 && e.getClientRects().length>0
          && getComputedStyle(e).visibility!=='hidden' && e.getBoundingClientRect().right>0 && e.getBoundingClientRect().bottom>0)
          .map(e=>(e.innerText||'').trim()).filter(Boolean).join('\\n')""")

    def text(self):
        return self.ev("document.body.innerText")

    def has_dialog(self):
        return bool(self.ev("!!document.querySelector('[role=dialog]')"))

    def close_dialogs(self):
        for _ in range(3):
            if self.has_dialog():
                self.key("Escape")
                time.sleep(0.5)

    def expand_dialog(self):
        """Déplie les zones défilantes de la fenêtre modale pour la capturer en entier (nécessite un viewport assez haut)."""
        self.ev("""(() => { const d=document.querySelector('[role=dialog]'); if(!d) return;
          for (let pass=0; pass<3; pass++) for (const e of [d, ...d.querySelectorAll('*')]) {
            if (e.scrollHeight > e.clientHeight + 4) { const s=getComputedStyle(e);
              if (/(auto|scroll|hidden)/.test(s.overflowY) && e.clientHeight > 100) {
                e.style.maxHeight='none'; e.style.height='auto'; e.style.overflowY='visible'; } } }
          // le conteneur (fenêtre) doit aussi pouvoir grandir
          const nav = [...d.querySelectorAll('button')].find(b => (b.innerText||'').trim().split('\\n')[0]==='General');
          let e = nav; while (e && e !== d.parentElement) { const r=e.getBoundingClientRect();
            if (r.width > 100) { e.style.maxHeight='none'; if (r.width > 600) { e.style.height='auto'; e.style.minHeight='720px'; } }
            e = e.parentElement; }
        })()""")
        time.sleep(0.6)

    def open_settings(self, section="General"):
        """Ouvre la fenêtre Réglages (Ctrl+,) sur une section ; retourne le rectangle de la fenêtre."""
        if not self.has_dialog():
            self.send("Input.dispatchKeyEvent", type="keyDown", key=",", code="Comma", modifiers=2, windowsVirtualKeyCode=188)
            self.send("Input.dispatchKeyEvent", type="keyUp", key=",", code="Comma", modifiers=2, windowsVirtualKeyCode=188)
            time.sleep(1.2)
        r = self.ev("""((name) => { const d=document.querySelector('[role=dialog]'); if(!d) return null;
          const els=[...d.querySelectorAll('button')].filter(e=>(e.innerText||'').trim().split('\\n')[0]===name);
          if(!els.length) return null; const r=els[0].getBoundingClientRect(); return [r.x+r.width/2,r.y+r.height/2]; })(%s)""" % json.dumps(section))
        if not r:
            raise LookupError("section de réglages introuvable : " + section)
        self.click_xy(*r)
        time.sleep(1.0)
        return self.dialog_clip()

    def dialog_scroller(self):
        """Retourne l'info du conteneur défilant principal de la fenêtre modale (ou None s'il n'y a pas de débordement)."""
        return self.ev("""(() => { const d=document.querySelector('[role=dialog]'); if(!d) return null;
          const c=[...d.querySelectorAll('*')].filter(e=>e.scrollHeight>e.clientHeight+20 && /(auto|scroll)/.test(getComputedStyle(e).overflowY) && e.clientWidth>300);
          if(!c.length) return null; const e=c[0]; e.setAttribute('data-scr','1'); return [e.scrollHeight, e.clientHeight]; })()""")

    def scroll_dialog(self, to):
        self.ev("(() => { const e=document.querySelector('[data-scr=\"1\"]'); if(e) e.scrollTop = %s; })()" % ("e.scrollHeight" if to == "end" else "0"))
        time.sleep(0.5)

    def shot_dialog(self, name, clip=None):
        """Capture la fenêtre modale ; si son contenu défile, ajoute une seconde capture <name>-suite.png (bas de page)."""
        clip = clip or self.dialog_clip()
        out = [self.shot(name, clip=clip)]
        if self.dialog_scroller():
            self.scroll_dialog("end")
            out.append(self.shot(name + "-suite", clip=clip))
            self.scroll_dialog("start")
        return out

    def wait(self, s=1.0):
        time.sleep(s)

    # --- captures ---------------------------------------------------------
    def annotate(self, items):
        """Superpose des cadres rouges numérotés. items = [(selector|None, text|None, label, nth)] ou [(x,y,w,h,label)]."""
        boxes = []
        for it in items:
            if len(it) in (5, 6) and isinstance(it[0], (int, float)):
                boxes.append(list(it))
            else:
                sel, txt, label = it[0], it[1], it[2]
                nth = it[3] if len(it) > 3 else 0
                r = self.rect(sel, txt, nth)
                if r:
                    boxes.append(r + [label])
        js = """((boxes) => {
          document.querySelectorAll('.__ann').forEach(e => e.remove());
          boxes.forEach(([x,y,w,h,l,pos]) => {
            const b = document.createElement('div'); b.className='__ann';
            b.style.cssText = `position:fixed;left:${x-3}px;top:${y-3}px;width:${w+6}px;height:${h+6}px;border:3px solid #e5322d;border-radius:6px;z-index:2147483646;pointer-events:none;box-shadow:0 0 0 1px #fff`;
            const n = document.createElement('div');
            n.textContent = l; n.style.cssText = `position:absolute;left:${pos==='r' ? (w-12)+'px' : Math.max(-14,5-x)+'px'};top:${Math.max(-14,5-y)}px;min-width:24px;height:24px;border-radius:12px;background:#e5322d;color:#fff;font:700 14px/24px Segoe UI,sans-serif;text-align:center;padding:0 5px;box-shadow:0 0 0 2px #fff`;
            b.appendChild(n); document.body.appendChild(b);
          });
        })(%s)""" % json.dumps(boxes)
        self.ev(js)

    def clear_annotations(self):
        self.ev("document.querySelectorAll('.__ann').forEach(e => e.remove())")

    MASK = ["Peux tu me traduire", "Unnamed Chat"]  # conversations préexistantes de l'utilisateur : jamais montrées

    def _mask(self, on=True):
        js = """((names, on) => {
          document.querySelectorAll('*').forEach(e => {
            if (e.children.length === 0 && names.includes((e.textContent || '').trim())) {
              if (on) { e.dataset.__m = e.style.visibility || '-'; e.style.visibility = 'hidden'; }
            } else if (!on && e.dataset && e.dataset.__m !== undefined) {
              e.style.visibility = e.dataset.__m === '-' ? '' : e.dataset.__m; delete e.dataset.__m;
            }
          });
        })(%s, %s)""" % (json.dumps(self.MASK), "true" if on else "false")
        self.ev(js)

    def dialog_clip(self, pad=0):
        r = self.ev("""(() => { const d=document.querySelector('[role=dialog]'); if(!d) return null;
          const full = innerWidth*innerHeight;
          const nav = [...d.querySelectorAll('button')].find(b => (b.innerText||'').trim().split('\\n')[0]==='General');
          let start = nav || d.querySelector('button, h1, h2, [class*=title]') || d;
          let e = start, best = null;
          while (e && e !== document.body) { const r=e.getBoundingClientRect();
            if (r.width > 600 && r.height > 300 && r.width*r.height < 0.97*full) { best = r; break; }
            e = e.parentElement; }
          if (!best) { const r = d.getBoundingClientRect(); if (r.width*r.height < 0.97*full) best = r; }
          return best ? [best.x,best.y,best.width,best.height] : null; })()""")
        return None if not r else (max(r[0] - pad, 0), max(r[1] - pad, 0), r[2] + 2 * pad, r[3] + 2 * pad)

    def shot(self, name, annotations=None, clip=None):
        """Capture PNG vers docs/img/<name>.png. clip=(x,y,w,h) pour recadrer."""
        import os
        self._mask(True)
        if annotations:
            self.annotate(annotations)
        time.sleep(0.4)
        params = dict(format="png")
        if clip:
            params["clip"] = dict(x=clip[0], y=clip[1], width=clip[2], height=clip[3], scale=1)
        data = self.send("Page.captureScreenshot", **params)["data"]
        path = os.path.join(DOCS_IMG, name if name.endswith(".png") else name + ".png")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(base64.b64decode(data))
        if annotations:
            self.clear_annotations()
        self._mask(False)
        return path
