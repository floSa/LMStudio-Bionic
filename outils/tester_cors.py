"""Teste le comportement CORS du serveur LM Studio : requête simple avec en-tête Origin, requête préalable (OPTIONS) d'un navigateur.

Usage : python tester_cors.py <etat>   (etat = off ou on : état du réglage « Enable CORS » au moment du test ; sert à nommer le résultat)
Un jeton facultatif est lu dans LMSTUDIO_TOKEN. Résultats : outils/resultats/lot2_cors_<etat>.json
"""
import json
import os
import sys
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:1234"
ETAT = sys.argv[1]
JETON = os.environ.get("LMSTUDIO_TOKEN")
ICI = os.path.dirname(os.path.abspath(__file__))
ORIGINE = "http://site-externe.example"


def appel(methode, chemin, entetes):
    req = urllib.request.Request(BASE + chemin, headers=entetes, method=methode, data=b"{}" if methode == "POST" else None)
    try:
        r = urllib.request.urlopen(req, timeout=30)
        status, h, corps = r.status, r.headers, r.read()[:120]
    except urllib.error.HTTPError as e:
        status, h, corps = e.code, e.headers, e.read()[:120]
    cors = {k: v for k, v in h.items() if k.lower().startswith("access-control")}
    return {"status": status, "en_tetes_cors": cors or "aucun", "corps": corps.decode("utf-8", "replace").replace("\n", " ")}


auth = {"Authorization": f"Bearer {JETON}"} if JETON else {}
res = {
    "GET /v1/models avec Origin (jeton valide)": appel("GET", "/v1/models", dict(auth, Origin=ORIGINE)),
    "GET /v1/models avec Origin (sans jeton)": appel("GET", "/v1/models", {"Origin": ORIGINE}),
    "OPTIONS /v1/chat/completions (requête préalable du navigateur)": appel("OPTIONS", "/v1/chat/completions", {
        "Origin": ORIGINE, "Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "authorization,content-type"}),
}
for k, v in res.items():
    print(v["status"], k, "|", v["en_tetes_cors"], flush=True)
with open(os.path.join(ICI, "resultats", f"lot2_cors_{ETAT}.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
