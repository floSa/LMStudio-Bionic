"""Embeddings (vecteurs de sens) avec le modèle text-embedding-nomic-embed-text-v1.5 et similarité cosinus.
Le chargement « Just-in-Time » doit être activé (par défaut) : le modèle d'embedding se charge à la première requête."""
import math
from lmstudio_client import post

EMB = "text-embedding-nomic-embed-text-v1.5"
phrases = [
    "La centrale produit de l'électricité.",
    "Une usine génère du courant électrique.",
    "Le chat dort sur le canapé.",
]
rep = post("/v1/embeddings", {"model": EMB, "input": phrases})
v = [d["embedding"] for d in rep["data"]]


def cos(a, b):
    return sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))


print(f"dimension des vecteurs : {len(v[0])}")
print(f"« {phrases[0]} » ~ « {phrases[1]} » : {cos(v[0], v[1]):.3f}")
print(f"« {phrases[0]} » ~ « {phrases[2]} » : {cos(v[0], v[2]):.3f}")
