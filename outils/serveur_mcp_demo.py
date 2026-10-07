"""Serveur MCP de démonstration : JSON-RPC 2.0 sur stdio, bibliothèque standard uniquement.

Sert à tester l'hôte MCP de LM Studio (mcp.json) et de Bionic sans installer de serveur tiers.
Chaque message est une ligne JSON sur l'entrée standard ; chaque réponse est une ligne JSON sur la sortie standard.
Les journaux vont sur la sortie d'erreur (jamais sur la sortie standard, réservée au protocole).

Outils exposés (tous inoffensifs) :
    convertir_temperature(valeur, de, vers)   conversion C / F / K
    calculer_statistiques(nombres)            minimum, maximum, moyenne, médiane
    lister_notes()                            noms des fichiers du dossier fictif outils/mcp_demo_notes/
    lire_note(nom)                            contenu d'un fichier de ce dossier (lecture seule, sans sortie du dossier)
    ecrire_note(nom, contenu)                 écrit un fichier .txt dans ce dossier (outil à effet de bord, pour tester la confirmation)

Mode distant : « python serveur_mcp_demo.py --http 8765 » écoute sur 127.0.0.1:8765 (transport HTTP, un POST par message).

Journal des appels : outils/resultats/mcp_demo_appels.log (une ligne par appel, utile pour prouver qu'un outil a été appelé).
"""
import json
import os
import statistics
import sys
import time

RACINE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.join(RACINE, "mcp_demo_notes")
JOURNAL = os.path.join(RACINE, "resultats", "mcp_demo_appels.log")

OUTILS = [
    {
        "name": "convertir_temperature",
        "description": "Convertit une température entre Celsius (C), Fahrenheit (F) et Kelvin (K).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "valeur": {"type": "number", "description": "Valeur à convertir"},
                "de": {"type": "string", "enum": ["C", "F", "K"], "description": "Unité de départ"},
                "vers": {"type": "string", "enum": ["C", "F", "K"], "description": "Unité d'arrivée"},
            },
            "required": ["valeur", "de", "vers"],
        },
    },
    {
        "name": "calculer_statistiques",
        "description": "Calcule le minimum, le maximum, la moyenne et la médiane d'une liste de nombres.",
        "inputSchema": {
            "type": "object",
            "properties": {"nombres": {"type": "array", "items": {"type": "number"}, "description": "Liste de nombres"}},
            "required": ["nombres"],
        },
    },
    {
        "name": "lister_notes",
        "description": "Liste les notes disponibles (fichiers texte du dossier de notes fictif).",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "lire_note",
        "description": "Renvoie le contenu d'une note texte du dossier de notes fictif.",
        "inputSchema": {
            "type": "object",
            "properties": {"nom": {"type": "string", "description": "Nom du fichier, par exemple reunion.txt"}},
            "required": ["nom"],
        },
    },
    {
        "name": "ecrire_note",
        "description": "Crée ou remplace une note texte (.txt) dans le dossier de notes fictif.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "nom": {"type": "string", "description": "Nom du fichier, extension .txt"},
                "contenu": {"type": "string", "description": "Texte à écrire"},
            },
            "required": ["nom", "contenu"],
        },
    },
]


def journaliser(texte):
    os.makedirs(os.path.dirname(JOURNAL), exist_ok=True)
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ") + texte + "\n")


def chemin_note(nom):
    """Chemin d'une note, refusé s'il sort du dossier de notes."""
    base = os.path.realpath(NOTES)
    chemin = os.path.realpath(os.path.join(base, nom))
    if os.path.dirname(chemin) != base:
        raise ValueError("nom de fichier refusé : sortie du dossier de notes")
    return chemin


def convertir_temperature(valeur, de, vers):
    kelvin = {"C": lambda v: v + 273.15, "F": lambda v: (v - 32) * 5 / 9 + 273.15, "K": lambda v: v}[de](valeur)
    res = {"C": lambda k: k - 273.15, "F": lambda k: (k - 273.15) * 9 / 5 + 32, "K": lambda k: k}[vers](kelvin)
    return f"{valeur} {de} = {round(res, 2)} {vers}"


def calculer_statistiques(nombres):
    if not nombres:
        raise ValueError("liste vide")
    return json.dumps({"minimum": min(nombres), "maximum": max(nombres),
                       "moyenne": round(statistics.mean(nombres), 4), "mediane": statistics.median(nombres),
                       "effectif": len(nombres)}, ensure_ascii=False)


def lister_notes():
    os.makedirs(NOTES, exist_ok=True)
    return "\n".join(sorted(os.listdir(NOTES))) or "(aucune note)"


def lire_note(nom):
    with open(chemin_note(nom), encoding="utf-8") as f:
        return f.read()


def ecrire_note(nom, contenu):
    if not nom.endswith(".txt"):
        raise ValueError("seules les notes .txt sont autorisées")
    os.makedirs(NOTES, exist_ok=True)
    with open(chemin_note(nom), "w", encoding="utf-8") as f:
        f.write(contenu)
    return f"note {nom} écrite ({len(contenu)} caractères)"


FONCTIONS = {o.__name__: o for o in (convertir_temperature, calculer_statistiques, lister_notes, lire_note, ecrire_note)}


def repondre(msg_id, resultat=None, erreur=None):
    rep = {"jsonrpc": "2.0", "id": msg_id}
    if erreur is not None:
        rep["error"] = erreur
    else:
        rep["result"] = resultat
    sys.stdout.write(json.dumps(rep, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def traiter(msg):
    methode, msg_id, params = msg.get("method"), msg.get("id"), msg.get("params") or {}
    if methode == "initialize":
        repondre(msg_id, {
            "protocolVersion": params.get("protocolVersion", "2025-06-18"),
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "serveur-mcp-demo", "version": "1.0"},
        })
    elif methode == "ping":
        repondre(msg_id, {})
    elif methode == "tools/list":
        repondre(msg_id, {"tools": OUTILS})
    elif methode == "tools/call":
        nom, args = params.get("name"), params.get("arguments") or {}
        journaliser(f"appel {nom} {json.dumps(args, ensure_ascii=False)}")
        try:
            if nom not in FONCTIONS:
                raise ValueError(f"outil inconnu : {nom}")
            texte = FONCTIONS[nom](**args)
            repondre(msg_id, {"content": [{"type": "text", "text": texte}], "isError": False})
        except Exception as e:  # erreur d'outil : renvoyée au modèle, pas une erreur de protocole
            journaliser(f"erreur {nom} : {e}")
            repondre(msg_id, {"content": [{"type": "text", "text": f"Erreur : {e}"}], "isError": True})
    elif msg_id is not None:  # méthode inconnue avec identifiant : erreur JSON-RPC standard
        repondre(msg_id, erreur={"code": -32601, "message": f"méthode inconnue : {methode}"})
    # les notifications (sans id), comme notifications/initialized, n'appellent aucune réponse


def main_http(port):
    """Mode « serveur distant » (transport HTTP, réponses JSON) : un POST par message JSON-RPC, uniquement sur 127.0.0.1."""
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class Gestionnaire(BaseHTTPRequestHandler):
        def do_POST(self):
            msg = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            self.entetes_recus = dict(self.headers)
            journaliser("http " + (msg.get("method") or "?") + " auth=" + ("oui" if self.headers.get("Authorization") else "non"))
            captured = []
            global repondre
            ancienne = repondre
            repondre = lambda msg_id, resultat=None, erreur=None: captured.append(
                {"jsonrpc": "2.0", "id": msg_id, **({"error": erreur} if erreur is not None else {"result": resultat})})
            try:
                traiter(msg)
            finally:
                repondre = ancienne
            corps = json.dumps(captured[0] if captured else {}, ensure_ascii=False).encode("utf-8")
            self.send_response(200 if captured else 202)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(corps)))
            self.end_headers()
            self.wfile.write(corps)

        def do_GET(self):  # pas de flux serveur -> client : 405 est la réponse prévue par le protocole
            self.send_response(405)
            self.end_headers()

        do_DELETE = do_GET

        def log_message(self, *a):
            pass

    HTTPServer(("127.0.0.1", port), Gestionnaire).serve_forever()


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--http":
        return main_http(int(sys.argv[2]))
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    for ligne in sys.stdin:
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            traiter(json.loads(ligne))
        except json.JSONDecodeError:
            repondre(None, erreur={"code": -32700, "message": "JSON invalide"})


if __name__ == "__main__":
    main()
