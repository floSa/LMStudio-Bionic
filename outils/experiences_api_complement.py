import json, time, urllib.request, urllib.error

BASE = "http://127.0.0.1:1234"

def call(path, body=None, headers=None, timeout=300):
    h = {"Content-Type": "application/json"}
    h.update(headers or {})
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode() if body is not None else None, headers=h)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers), json.load(r), round(time.time() - t0, 2)
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read().decode()[:400], round(time.time() - t0, 2)

# API native /api/v1/chat
s, h, o, t = call("/api/v1/chat", {"model": "google/gemma-4-e4b", "input": "Réponds par un seul mot : capitale de l'Italie ?", "reasoning": "off", "temperature": 0, "max_output_tokens": 50})
print("NATIVE /api/v1/chat", s, t, "s"); print(json.dumps(o, ensure_ascii=False, indent=1)[:1500])

# Anthropic /v1/messages
s, h, o, t = call("/v1/messages", {"model": "google/gemma-4-e4b", "max_tokens": 60, "messages": [{"role": "user", "content": "Réponds par un seul mot : capitale de l'Espagne ?"}], "temperature": 0})
print("\nANTHROPIC /v1/messages", s, t, "s"); print(json.dumps(o, ensure_ascii=False, indent=1)[:1200])

# Responses
s, h, o, t = call("/v1/responses", {"model": "google/gemma-4-e4b", "input": "Réponds par un seul mot : capitale du Portugal ?", "max_output_tokens": 60, "reasoning": {"effort": "none"}})
print("\nRESPONSES /v1/responses", s, t, "s"); print(json.dumps(o, ensure_ascii=False, indent=1)[:1200] if not isinstance(o, str) else o)

# CORS : en-têtes de réponse avec un Origin externe
s, h, o, t = call("/v1/models", headers={"Origin": "http://site-externe.example"})
print("\nCORS (Origin externe) :", s, {k: v for k, v in h.items() if "access-control" in k.lower()} or "aucun en-tête Access-Control-*")

# Modèle inconnu
s, h, o, t = call("/v1/chat/completions", {"model": "modele-inexistant", "messages": [{"role": "user", "content": "x"}]})
print("\nMODELE INCONNU :", s, o if isinstance(o, str) else json.dumps(o)[:300])
