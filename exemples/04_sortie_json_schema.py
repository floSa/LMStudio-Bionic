"""Sortie structurée : le modèle est contraint de produire un JSON conforme à un schéma (response_format = json_schema)."""
import json
from lmstudio_client import chat

schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "facture",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "numero": {"type": "string"},
                "date": {"type": "string"},
                "client": {"type": "string"},
                "total_ttc": {"type": "number"},
            },
            "required": ["numero", "date", "client", "total_ttc"],
            "additionalProperties": False,
        },
    },
}
texte = "Facture F-2026-0042 du 06/10/2026 pour Atelier Démo SARL. Total TTC : 3 060,00 euros."
rep = chat(
    [{"role": "user", "content": "Extrais les informations de ce texte : " + texte}],
    response_format=schema, temperature=0, max_tokens=300, reasoning_effort="none",
)
donnees = json.loads(rep["choices"][0]["message"]["content"])   # toujours du JSON valide grâce au schéma
print(json.dumps(donnees, ensure_ascii=False, indent=2))
