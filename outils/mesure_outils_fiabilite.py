"""Mesure la fiabilité de l'appel d'outils d'un modèle local via /v1/chat/completions.

Les cinq outils sont ceux du serveur MCP de démonstration (serveur_mcp_demo.py). Chaque consigne est jouée N fois à
température 0,7 ; le script vérifie : outil attendu appelé, arguments conformes au schéma et à la valeur attendue.
Aucun outil n'est exécuté (la mesure porte sur la décision et le format de l'appel).

Usage : python mesure_outils_fiabilite.py <identifiant_modele> [N]
Sortie : outils/resultats/lot2_outils_<modele>.json
"""
import json
import os
import re
import sys
import time
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import serveur_mcp_demo as srv  # noqa: E402  (importé pour réutiliser les schémas d'outils)

BASE = os.environ.get("LMSTUDIO_URL", "http://127.0.0.1:1234")
TOKEN = os.environ.get("LMSTUDIO_TOKEN")
MODELE = sys.argv[1] if len(sys.argv) > 1 else "google/gemma-4-e4b"
N = int(sys.argv[2]) if len(sys.argv) > 2 else 4
DIFFICILE = os.environ.get("DIFFICILE") == "1"   # ajoute 12 outils proches (distracteurs) et des consignes plus ambiguës

OUTILS = [{"type": "function", "function": {"name": o["name"], "description": o["description"], "parameters": o["inputSchema"]}}
          for o in srv.OUTILS]

def _outil(nom, desc, props, requis):
    return {"type": "function", "function": {"name": nom, "description": desc,
                                              "parameters": {"type": "object", "properties": props, "required": requis}}}


DISTRACTEURS = [
    _outil("convertir_longueur", "Convertit une longueur entre m, km, mi et ft.", {"valeur": {"type": "number"}, "de": {"type": "string"}, "vers": {"type": "string"}}, ["valeur", "de", "vers"]),
    _outil("convertir_masse", "Convertit une masse entre kg, g, lb et oz.", {"valeur": {"type": "number"}, "de": {"type": "string"}, "vers": {"type": "string"}}, ["valeur", "de", "vers"]),
    _outil("calculer_moyenne", "Calcule uniquement la moyenne d'une liste de nombres.", {"nombres": {"type": "array", "items": {"type": "number"}}}, ["nombres"]),
    _outil("calculer_mediane", "Calcule uniquement la médiane d'une liste de nombres.", {"nombres": {"type": "array", "items": {"type": "number"}}}, ["nombres"]),
    _outil("supprimer_note", "Supprime une note texte.", {"nom": {"type": "string"}}, ["nom"]),
    _outil("renommer_note", "Renomme une note texte.", {"ancien": {"type": "string"}, "nouveau": {"type": "string"}}, ["ancien", "nouveau"]),
    _outil("rechercher_dans_notes", "Cherche un mot dans toutes les notes.", {"mot": {"type": "string"}}, ["mot"]),
    _outil("lire_fichier", "Lit un fichier quelconque du disque.", {"chemin": {"type": "string"}}, ["chemin"]),
    _outil("heure_locale", "Donne l'heure locale d'une ville.", {"ville": {"type": "string"}}, ["ville"]),
    _outil("meteo", "Donne la météo d'une ville.", {"ville": {"type": "string"}}, ["ville"]),
    _outil("envoyer_courriel", "Envoie un courriel.", {"destinataire": {"type": "string"}, "objet": {"type": "string"}, "corps": {"type": "string"}}, ["destinataire", "objet", "corps"]),
    _outil("traduire", "Traduit un texte vers une langue cible.", {"texte": {"type": "string"}, "langue": {"type": "string"}}, ["texte", "langue"]),
]
if DIFFICILE:
    OUTILS = OUTILS + DISTRACTEURS

# (consigne, outil attendu ou None, vérificateur d'arguments)
CAS = [
    ("Convertis 37 degrés Celsius en Kelvin.", "convertir_temperature",
     lambda a: a.get("de") == "C" and a.get("vers") == "K" and abs(float(a.get("valeur", 0)) - 37) < 1e-9),
    ("Combien font 98,6 degrés Fahrenheit en Celsius ?", "convertir_temperature",
     lambda a: a.get("de") == "F" and a.get("vers") == "C" and abs(float(a.get("valeur", 0)) - 98.6) < 1e-9),
    ("Donne les statistiques de la série 5, 1, 9, 3, 12.", "calculer_statistiques",
     lambda a: sorted(a.get("nombres", [])) == [1, 3, 5, 9, 12]),
    ("Quelles notes sont disponibles ?", "lister_notes", lambda a: True),
    ("Lis la note courses.txt.", "lire_note", lambda a: a.get("nom") == "courses.txt"),
    ("Enregistre une note rappel.txt contenant : Appeler le fournisseur.", "ecrire_note",
     lambda a: a.get("nom") == "rappel.txt" and "fournisseur" in a.get("contenu", "").lower()),
    ("Quelle est la capitale du Portugal ?", None, lambda a: True),
    ("Il fait 20 degrés dehors : faut-il prendre une veste ?", None, lambda a: True),
]


def appeler(consigne):
    corps = {"model": MODELE, "messages": [{"role": "user", "content": consigne}], "tools": OUTILS,
             "temperature": 0.7, "max_tokens": 600, "reasoning_effort": "none"}
    h = {"Content-Type": "application/json"}
    if TOKEN:
        h["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(BASE + "/v1/chat/completions", data=json.dumps(corps).encode(), headers=h)
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as r:
        o = json.load(r)
    return o, time.time() - t0


if DIFFICILE:
    CAS = CAS + [
        ("Quelle est la moyenne de 4 et 8 ?", "calculer_moyenne", lambda a: sorted(a.get("nombres", [])) == [4, 8]),
        ("Convertis 5 kilomètres en miles.", "convertir_longueur", lambda a: a.get("de") == "km" and a.get("vers") == "mi"),
        ("Supprime la note courses.txt.", "supprimer_note", lambda a: a.get("nom") == "courses.txt"),
        ("Y a-t-il une note qui parle du budget ?", "rechercher_dans_notes", lambda a: "budget" in a.get("mot", "").lower()),
        ("Convertis 100 en Fahrenheit.", None, lambda a: True),   # unité de départ absente : poser une question ou deviner (tout appel = inutile)
    ]

resultats = []
for consigne, attendu, verif in CAS:
    for i in range(N):
        o, dt = appeler(consigne)
        m = o["choices"][0]["message"]
        appels = m.get("tool_calls") or []
        noms = [c["function"]["name"] for c in appels]
        statut, detail = "", ""
        if attendu is None:
            statut = "correct" if not appels else "appel_inutile"
            detail = (m.get("content") or "")[:120] if not appels else noms
        elif not appels:
            # appel non reconnu : le texte contient-il un appel mal formé ?
            txt = m.get("content") or ""
            statut = "appel_mal_forme" if re.search(attendu, txt) or "tool" in txt.lower() else "aucun_appel"
            detail = txt[:160]
        else:
            c = appels[0]["function"]
            try:
                args = json.loads(c["arguments"])
            except json.JSONDecodeError:
                args, statut, detail = {}, "json_invalide", c["arguments"][:120]
            if not statut:
                if c["name"] != attendu:
                    statut, detail = "mauvais_outil", c["name"]
                elif verif(args):
                    statut, detail = "correct", args
                else:
                    statut, detail = "arguments_incorrects", args
        resultats.append({"consigne": consigne, "attendu": attendu, "statut": statut, "detail": detail,
                          "secondes": round(dt, 1), "tokens": o["usage"]["completion_tokens"]})
        print(f"{statut:22s} {dt:5.1f}s  {consigne[:50]}  {str(detail)[:60]}", flush=True)

total = len(resultats)
ok = sum(1 for r in resultats if r["statut"] == "correct")
par_statut = {}
for r in resultats:
    par_statut[r["statut"]] = par_statut.get(r["statut"], 0) + 1
synthese = {"modele": MODELE, "difficile": DIFFICILE, "outils_declares": len(OUTILS), "essais": total, "corrects": ok, "taux": round(ok / total, 3), "par_statut": par_statut,
            "secondes_moyennes": round(sum(r["secondes"] for r in resultats) / total, 1)}
print(json.dumps(synthese, ensure_ascii=False))
nom = re.sub(r"[^a-z0-9]+", "_", MODELE.lower()).strip("_") + ("_difficile" if DIFFICILE else "")
with open(os.path.join(ICI, "resultats", f"lot2_outils_{nom}.json"), "w", encoding="utf-8") as f:
    json.dump({"synthese": synthese, "essais": resultats}, f, ensure_ascii=False, indent=1)
