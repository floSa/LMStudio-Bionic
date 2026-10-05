"""Mini-client pour l'API locale de LM Studio (compatible OpenAI). Aucune dépendance : bibliothèque standard uniquement.

Variables d'environnement facultatives :
    LMSTUDIO_URL    adresse du serveur            (défaut : http://127.0.0.1:1234)
    LMSTUDIO_MODEL  identifiant du modèle         (défaut : google/gemma-4-e4b)
    LMSTUDIO_TOKEN  jeton d'API si l'authentification est activée (défaut : aucun)
"""
import base64
import json
import mimetypes
import os
import urllib.error
import urllib.request

BASE = os.environ.get("LMSTUDIO_URL", "http://127.0.0.1:1234").rstrip("/")
MODEL = os.environ.get("LMSTUDIO_MODEL", "google/gemma-4-e4b")
TOKEN = os.environ.get("LMSTUDIO_TOKEN")


def _request(path, body=None, stream=False, timeout=900):
    headers = {"Content-Type": "application/json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code} : {e.read().decode('utf-8', 'replace')[:500]}") from None
    except urllib.error.URLError as e:
        raise RuntimeError(f"Serveur LM Studio injoignable sur {BASE} ({e.reason}). Le serveur est-il démarré ?") from None
    return resp if stream else json.load(resp)


def get(path):
    return _request(path)


def post(path, body):
    return _request(path, body)


def chat(messages, **params):
    """Appelle /v1/chat/completions et retourne la réponse JSON complète."""
    body = {"model": MODEL, "messages": messages}
    body.update(params)
    return post("/v1/chat/completions", body)


def chat_stream(messages, **params):
    """Générateur : produit les morceaux de texte au fur et à mesure (SSE)."""
    body = {"model": MODEL, "messages": messages, "stream": True}
    body.update(params)
    with _request("/v1/chat/completions", body, stream=True) as resp:
        for raw in resp:
            line = raw.decode("utf-8").strip()
            if not line.startswith("data:") or line.endswith("[DONE]"):
                continue
            chunk = json.loads(line[5:])
            if chunk.get("choices"):
                piece = chunk["choices"][0]["delta"].get("content")
                if piece:
                    yield piece


def image_part(path):
    """Contenu 'image_url' (data URL base64) pour un fichier image local."""
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}
