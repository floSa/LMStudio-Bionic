"""Réponse en flux (SSE) : affiche les mots au fur et à mesure et mesure le délai avant le premier token (TTFT)."""
import time
from lmstudio_client import chat_stream

t0 = time.time()
premier = None
n = 0
for morceau in chat_stream(
    [{"role": "user", "content": "Compte de 1 à 20 en français, séparés par des virgules."}],
    temperature=0, max_tokens=120, reasoning_effort="none",
):
    if premier is None:
        premier = time.time() - t0
    n += 1
    print(morceau, end="", flush=True)
print(f"\n\nTTFT = {premier:.2f} s ; {n} morceaux en {time.time() - t0:.2f} s")
