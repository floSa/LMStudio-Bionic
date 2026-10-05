"""Liste les modèles visibles par le serveur LM Studio (GET /v1/models et GET /api/v1/models)."""
from lmstudio_client import get

print("== API compatible OpenAI : /v1/models")
for m in get("/v1/models")["data"]:
    print(" -", m["id"])

print("\n== API native LM Studio : /api/v1/models")
for m in get("/api/v1/models")["models"]:
    loaded = [i["id"] for i in m.get("loaded_instances", [])]
    print(f" - {m['key']:45s} type={m['type']:9s} taille={m['size_bytes']/1e9:5.2f} Go  contexte max={m.get('max_context_length')}  chargé={bool(loaded)}")
    for inst in m.get("loaded_instances", []):
        cfg = inst["config"]
        print(f"     instance {inst['id']} : contexte={cfg.get('context_length')}, parallèle={cfg.get('parallel')}, flash_attention={cfg.get('flash_attention')}")
