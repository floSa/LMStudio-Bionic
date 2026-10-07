"""Teste l'authentification du serveur LM Studio (en-têtes, jetons absents, faux ou valides) et les permissions MCP d'un jeton.

Le jeton est lu dans la variable d'environnement LMSTUDIO_TOKEN (jeton factice créé pour le test, supprimé ensuite) ; il n'est jamais
écrit dans les résultats. Usage : LMSTUDIO_TOKEN=... python tester_authentification.py <nom_du_scenario>
Résultats : outils/resultats/lot2_auth_<scenario>.json
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:1234"
JETON = os.environ["LMSTUDIO_TOKEN"]
SCENARIO = sys.argv[1] if len(sys.argv) > 1 else "jeton"
ICI = os.path.dirname(os.path.abspath(__file__))


def appel(methode, chemin, corps=None, entetes=None):
    h = {"Content-Type": "application/json"}
    h.update(entetes or {})
    req = urllib.request.Request(BASE + chemin, data=json.dumps(corps).encode() if corps is not None else None, headers=h, method=methode)
    t0 = time.time()
    try:
        r = urllib.request.urlopen(req, timeout=300)
        brut = r.read().decode("utf-8", "replace")
        return {"status": r.status, "secondes": round(time.time() - t0, 1), "corps": brut[:300].replace("\n", " ")}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "secondes": round(time.time() - t0, 1), "corps": e.read().decode("utf-8", "replace")[:300].replace("\n", " "),
                "www_authenticate": e.headers.get("WWW-Authenticate")}


def masque(x):
    return json.loads(json.dumps(x).replace(JETON, "<JETON>"))


MSG = {"model": "google/gemma-4-e4b", "messages": [{"role": "user", "content": "Dis ok."}], "max_tokens": 8, "reasoning_effort": "none", "temperature": 0}
ANTH = {"model": "google/gemma-4-e4b", "max_tokens": 8, "messages": [{"role": "user", "content": "Dis ok."}]}
cas = {
    "GET /v1/models sans en-tête": ("GET", "/v1/models", None, {}),
    "GET /v1/models, mauvais jeton": ("GET", "/v1/models", None, {"Authorization": "Bearer sk-lm-faux:faux"}),
    "GET /v1/models, Authorization incorrect (sans Bearer)": ("GET", "/v1/models", None, {"Authorization": JETON}),
    "GET /v1/models, bon jeton": ("GET", "/v1/models", None, {"Authorization": f"Bearer {JETON}"}),
    "GET /api/v1/models, bon jeton": ("GET", "/api/v1/models", None, {"Authorization": f"Bearer {JETON}"}),
    "POST /v1/chat/completions sans en-tête": ("POST", "/v1/chat/completions", MSG, {}),
    "POST /v1/chat/completions, bon jeton": ("POST", "/v1/chat/completions", MSG, {"Authorization": f"Bearer {JETON}"}),
    "POST /v1/messages, en-tête x-api-key": ("POST", "/v1/messages", ANTH, {"x-api-key": JETON, "anthropic-version": "2023-06-01"}),
    "POST /v1/messages, x-api-key factice": ("POST", "/v1/messages", ANTH, {"x-api-key": "factice", "anthropic-version": "2023-06-01"}),
    "POST /api/v1/chat, bon jeton": ("POST", "/api/v1/chat", {"model": "google/gemma-4-e4b", "input": "Dis ok.", "reasoning": "off", "max_output_tokens": 8, "store": False}, {"Authorization": f"Bearer {JETON}"}),
    "POST /api/v1/chat + mcp/demo-notes (plugin)": ("POST", "/api/v1/chat", {"model": "google/gemma-4-e4b", "input": "Convertis 100 degrés Celsius en Fahrenheit avec l'outil.", "reasoning": "off", "max_output_tokens": 300, "store": False,
                                                    "integrations": [{"type": "plugin", "id": "mcp/demo-notes", "allowed_tools": ["convertir_temperature"]}]}, {"Authorization": f"Bearer {JETON}"}),
}
res = {}
for nom, (m, p, c, h) in cas.items():
    r = appel(m, p, c, h)
    res[nom] = masque(r)
    print(r["status"], nom, "|", r["corps"][:150], flush=True)
with open(os.path.join(ICI, "resultats", f"lot2_auth_{SCENARIO}.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
