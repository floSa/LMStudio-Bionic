"""MCP par l'API REST de LM Studio : serveur de mcp.json (« plugin ») et serveur distant à la volée (« ephemeral_mcp »).

Prérequis : authentification activée, jeton avec la permission « Allow calling servers from mcp.json » dans LMSTUDIO_TOKEN,
réglages serveur « Allow calling servers from mcp.json » et « Allow per-request MCPs » activés, serveur « demo-notes » déclaré
dans mcp.json. Le serveur distant de démonstration est lancé par ce script sur 127.0.0.1:8765.
Résultats : outils/resultats/lot2_mcp_api.json (le jeton n'y figure pas).
"""
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
BASE = "http://127.0.0.1:1234"
JETON = os.environ["LMSTUDIO_TOKEN"]
MODELE = "google/gemma-4-e4b"


def post(corps, flux=False):
    req = urllib.request.Request(BASE + "/api/v1/chat", data=json.dumps(corps).encode(),
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {JETON}"})
    t0 = time.time()
    try:
        r = urllib.request.urlopen(req, timeout=600)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode()), round(time.time() - t0, 1)
    if not flux:
        return r.status, json.load(r), round(time.time() - t0, 1)
    evts = []
    for brut in r:
        ligne = brut.decode("utf-8").strip()
        if ligne.startswith("data:"):
            try:
                evts.append(json.loads(ligne[5:]))
            except json.JSONDecodeError:
                pass
    return r.status, evts, round(time.time() - t0, 1)


def resume_sortie(o):
    out = []
    for i in o.get("output", []):
        if i["type"] == "tool_call":
            out.append({"type": "tool_call", "tool": i.get("tool"), "arguments": i.get("arguments"), "output": (i.get("output") or "")[:120], "provider_info": i.get("provider_info")})
        elif i["type"] == "message":
            out.append({"type": "message", "content": i["content"][:200]})
        else:
            out.append({"type": i["type"], "extrait": json.dumps(i, ensure_ascii=False)[:160]})
    return out


base = {"model": MODELE, "reasoning": "off", "temperature": 0, "max_output_tokens": 400, "store": False}
res = {}

s, o, t = post(dict(base, input="Convertis 100 degrés Celsius en Fahrenheit avec l'outil.",
                    integrations=[{"type": "plugin", "id": "mcp/demo-notes", "allowed_tools": ["convertir_temperature"]}]))
res["plugin_un_outil"] = {"status": s, "secondes": t, "sortie": resume_sortie(o) if s == 200 else o, "stats": o.get("stats") if s == 200 else None}

s, o, t = post(dict(base, input="Liste les notes disponibles puis lis courses.txt et indique ce qu'elle contient.", integrations=["mcp/demo-notes"]))
res["plugin_forme_courte_plusieurs_outils"] = {"status": s, "secondes": t, "sortie": resume_sortie(o) if s == 200 else o}

s, o, t = post(dict(base, input="Combien font 100 degrés Celsius en Fahrenheit ?", integrations=[{"type": "plugin", "id": "mcp/demo-notes", "allowed_tools": ["lister_notes"]}]))
res["outil_non_autorise"] = {"status": s, "sortie": resume_sortie(o) if s == 200 else o}

s, o, t = post(dict(base, input="Bonjour", integrations=[{"type": "plugin", "id": "mcp/inexistant"}]))
res["plugin_inexistant"] = {"status": s, "corps": o}

s, ev, t = post(dict(base, input="Quelle est la moyenne de 4, 8 et 15 ?", stream=True,
                     integrations=[{"type": "plugin", "id": "mcp/demo-notes", "allowed_tools": ["calculer_statistiques"]}]), flux=True)
res["flux_types"] = {"status": s, "secondes": t, "types": [e.get("type") for e in ev if e.get("type") not in ("message.delta", "reasoning.delta", "prompt_processing.progress")]}

# serveur distant à la volée
srv = subprocess.Popen([sys.executable, os.path.join(ICI, "serveur_mcp_demo.py"), "--http", "8765"])
time.sleep(1.5)
try:
    s, o, t = post(dict(base, input="Convertis 0 degré Celsius en Kelvin avec l'outil.",
                        integrations=[{"type": "ephemeral_mcp", "server_label": "demo-http", "server_url": "http://127.0.0.1:8765/mcp",
                                       "allowed_tools": ["convertir_temperature"], "headers": {"Authorization": "Bearer jeton-distant-factice"}}]))
    res["ephemeral_mcp_local"] = {"status": s, "secondes": t, "sortie": resume_sortie(o) if s == 200 else o}
finally:
    srv.kill()
for k, v in res.items():
    print(k, json.dumps(v, ensure_ascii=False)[:420], flush=True)
with open(os.path.join(ICI, "resultats", "lot2_mcp_api.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
