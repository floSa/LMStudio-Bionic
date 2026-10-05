"""OCR d'une image avec un modèle de vision (Gemma 4 E4B par défaut).
Usage : python 06_ocr_image.py [chemin_image]   (défaut : la facture fictive fournie dans ../outils/resultats/)."""
import os
import sys
import time
from lmstudio_client import chat, image_part

defaut = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outils", "resultats", "facture_test_1288.png")
chemin = sys.argv[1] if len(sys.argv) > 1 else defaut

prompt = ("Transcris fidèlement tout le texte de ce document en Markdown (conserve les tableaux). "
          "Ne rajoute aucun commentaire.")
t0 = time.time()
rep = chat(
    # Image AVANT le texte : ordre recommandé pour Gemma 4
    [{"role": "user", "content": [image_part(chemin), {"type": "text", "text": prompt}]}],
    temperature=0, max_tokens=1500, reasoning_effort="none",
)
print(rep["choices"][0]["message"]["content"])
u = rep["usage"]
print(f"\n[{u['prompt_tokens']} tokens en entrée (dont l'image), {u['completion_tokens']} en sortie, {time.time() - t0:.1f} s]")
