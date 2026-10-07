"""Client MCP minimal : lance serveur_mcp_demo.py, joue le protocole (initialize, tools/list, tools/call) et affiche les échanges.
Vérifie le serveur indépendamment de toute application hôte."""
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
p = subprocess.Popen([sys.executable, os.path.join(ICI, "serveur_mcp_demo.py")], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, text=True, encoding="utf-8")


def echange(msg):
    p.stdin.write(json.dumps(msg, ensure_ascii=False) + "\n")
    p.stdin.flush()
    if "id" not in msg:
        return None
    rep = json.loads(p.stdout.readline())
    print(">>", json.dumps(msg, ensure_ascii=False)[:150])
    print("<<", json.dumps(rep, ensure_ascii=False)[:300])
    return rep


echange({"jsonrpc": "2.0", "id": 1, "method": "initialize",
         "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "0"}}})
echange({"jsonrpc": "2.0", "method": "notifications/initialized"})
r = echange({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
assert [t["name"] for t in r["result"]["tools"]] == ["convertir_temperature", "calculer_statistiques", "lister_notes", "lire_note", "ecrire_note"]
r = echange({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "convertir_temperature", "arguments": {"valeur": 100, "de": "C", "vers": "F"}}})
assert "212" in r["result"]["content"][0]["text"]
r = echange({"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "calculer_statistiques", "arguments": {"nombres": [3, 9, 4, 10]}}})
assert '"moyenne": 6.5' in r["result"]["content"][0]["text"]
r = echange({"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "lire_note", "arguments": {"nom": "reunion.txt"}}})
assert "Budget" in r["result"]["content"][0]["text"]
r = echange({"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "lire_note", "arguments": {"nom": "..\\serveur_mcp_demo.py"}}})
assert r["result"]["isError"], "la sortie du dossier doit être refusée"
r = echange({"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": "lire_note", "arguments": {"nom": "..\\..\\README.md"}}})
assert r["result"]["isError"]
p.stdin.close()
p.wait(timeout=5)
print("OK : serveur MCP conforme au protocole de base")
