"""Rejoue, sans installer aucun outil, les requêtes que les clients tiers envoient au serveur LM Studio.

Aucun de ces outils n'est lancé : le script envoie des requêtes HTTP de même forme (route, en-têtes d'authentification,
options de flux, outils) que celles décrites dans leur documentation, afin de vérifier que le serveur les accepte.
Le résultat prouve la compatibilité de la route et du format, pas le comportement de l'outil lui-même.

Usage : python simuler_clients_tiers.py [jeton]
Résultats : outils/resultats/lot2_clients_tiers.json
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:1234"
MODELE = "google/gemma-4-e4b"
JETON = sys.argv[1] if len(sys.argv) > 1 else None
ICI = os.path.dirname(os.path.abspath(__file__))

OUTIL_OPENAI = {"type": "function", "function": {"name": "lire_fichier", "description": "Lit un fichier",
                                                  "parameters": {"type": "object", "properties": {"chemin": {"type": "string"}}, "required": ["chemin"]}}}


def requete(methode, chemin, corps=None, entetes=None, flux=False):
    h = {"Content-Type": "application/json"}
    h.update(entetes or {})
    data = json.dumps(corps).encode() if corps is not None else None
    req = urllib.request.Request(BASE + chemin, data=data, headers=h, method=methode)
    t0 = time.time()
    try:
        r = urllib.request.urlopen(req, timeout=300)
        brut = r.read().decode("utf-8", "replace")
        return {"status": r.status, "secondes": round(time.time() - t0, 1), "extrait": brut[:260].replace("\n", " ")}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "secondes": round(time.time() - t0, 1), "extrait": e.read().decode("utf-8", "replace")[:260].replace("\n", " ")}
    except Exception as e:  # noqa: BLE001
        return {"status": None, "extrait": str(e)[:200]}


cle = JETON or "lm-studio"   # clé factice usuelle des clients quand l'authentification est désactivée
bearer = {"Authorization": f"Bearer {cle}"}
cas = {
    "Claude Code : POST /v1/messages (flux, outils, système en blocs, x-api-key)": ("POST", "/v1/messages", {
        "model": MODELE, "max_tokens": 64, "stream": True, "temperature": 0,
        "system": [{"type": "text", "text": "Réponds en un mot.", "cache_control": {"type": "ephemeral"}}],
        "tools": [{"name": "lire_fichier", "description": "Lit un fichier", "input_schema": {"type": "object", "properties": {"chemin": {"type": "string"}}, "required": ["chemin"]}}],
        "metadata": {"user_id": "demo"}, "messages": [{"role": "user", "content": [{"type": "text", "text": "Dis ok."}]}]},
        {"x-api-key": cle, "anthropic-version": "2023-06-01", "anthropic-beta": "interleaved-thinking-2025-05-14"}),
    "Claude Code : POST /v1/messages/count_tokens": ("POST", "/v1/messages/count_tokens", {
        "model": MODELE, "messages": [{"role": "user", "content": "Bonjour"}]}, {"x-api-key": cle, "anthropic-version": "2023-06-01"}),
    "Codex : POST /v1/responses (flux, outil, store=false)": ("POST", "/v1/responses", {
        "model": MODELE, "input": [{"type": "message", "role": "user", "content": [{"type": "input_text", "text": "Dis ok."}]}],
        "tools": [{"type": "function", "name": "lire_fichier", "description": "Lit un fichier", "parameters": {"type": "object", "properties": {"chemin": {"type": "string"}}, "required": ["chemin"]}}],
        "stream": True, "store": False, "max_output_tokens": 64, "reasoning": {"effort": "none"}}, bearer),
    "Cline / Roo Code / Open WebUI : GET /v1/models": ("GET", "/v1/models", None, bearer),
    "Cline / Roo Code : GET /api/v0/models (ancienne API REST)": ("GET", "/api/v0/models", None, bearer),
    "Cline / Roo Code / Open WebUI : POST /v1/chat/completions (flux, usage)": ("POST", "/v1/chat/completions", {
        "model": MODELE, "stream": True, "stream_options": {"include_usage": True}, "max_tokens": 32, "temperature": 0, "reasoning_effort": "none",
        "messages": [{"role": "system", "content": "Réponds en un mot."}, {"role": "user", "content": "Dis ok."}]}, bearer),
    "Continue : POST /v1/chat/completions (outil)": ("POST", "/v1/chat/completions", {
        "model": MODELE, "max_tokens": 64, "temperature": 0, "reasoning_effort": "none", "tools": [OUTIL_OPENAI],
        "messages": [{"role": "user", "content": "Dis ok."}]}, bearer),
    "Continue (autocomplétion) : POST /v1/completions": ("POST", "/v1/completions", {
        "model": MODELE, "prompt": "def somme(a, b):\n    return", "max_tokens": 8, "temperature": 0}, bearer),
    "Continue (indexation) : POST /v1/embeddings": ("POST", "/v1/embeddings", {
        "model": "text-embedding-nomic-embed-text-v1.5", "input": "exemple"}, bearer),
    "Aider (litellm) : POST /v1/chat/completions, clé factice 'dummy-api-key'": ("POST", "/v1/chat/completions", {
        "model": MODELE, "max_tokens": 16, "temperature": 0, "reasoning_effort": "none", "messages": [{"role": "user", "content": "Dis ok."}]},
        {"Authorization": "Bearer dummy-api-key"}),
}
res = {}
for nom, (m, p, c, h) in cas.items():
    r = requete(m, p, c, h)
    res[nom] = r
    print(r["status"], f"{r.get('secondes', '')}s", nom, "|", r["extrait"][:110], flush=True)
suffixe = "_avec_jeton" if JETON else ""
with open(os.path.join(ICI, "resultats", f"lot2_clients_tiers{suffixe}.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
