"""Appel d'outil (function calling) : le modèle décide d'appeler une fonction et renvoie ses arguments en JSON.
C'est à VOTRE code d'exécuter la fonction, puis de renvoyer le résultat au modèle (non montré ici)."""
import json
from lmstudio_client import chat

outils = [{
    "type": "function",
    "function": {
        "name": "get_meteo",
        "description": "Donne la météo d'une ville",
        "parameters": {"type": "object", "properties": {"ville": {"type": "string"}}, "required": ["ville"]},
    },
}]
rep = chat([{"role": "user", "content": "Quel temps fait-il à Lyon ?"}],
           tools=outils, temperature=0, max_tokens=300, reasoning_effort="none")
choix = rep["choices"][0]
print("finish_reason :", choix["finish_reason"])
for appel in choix["message"].get("tool_calls", []):
    print("fonction demandée :", appel["function"]["name"], "avec", json.loads(appel["function"]["arguments"]))
