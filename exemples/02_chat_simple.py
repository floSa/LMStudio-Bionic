"""Une question, une réponse (POST /v1/chat/completions), avec lecture de l'usage en tokens."""
import time
from lmstudio_client import chat

t0 = time.time()
rep = chat(
    [
        {"role": "system", "content": "Tu es un assistant technique. Réponds en français, en deux phrases maximum."},
        {"role": "user", "content": "À quoi sert la quantification d'un modèle de langage ?"},
    ],
    temperature=0.3,        # peu de créativité : réponses stables
    max_tokens=300,         # coupe la réponse au-delà (finish_reason = "length")
    reasoning_effort="none" # coupe la phase de réflexion de Gemma 4 : réponse plus rapide
)
dt = time.time() - t0
msg = rep["choices"][0]["message"]
usage = rep["usage"]
print(msg["content"])
print(f"\n[{rep['choices'][0]['finish_reason']}] {usage['prompt_tokens']} tokens en entrée, "
      f"{usage['completion_tokens']} en sortie, {dt:.1f} s ({usage['completion_tokens']/dt:.1f} tok/s global)")
