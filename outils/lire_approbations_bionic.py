"""Relit, dans la base de sessions d'un projet Bionic, la façon dont chaque commande shell a été approuvée.

Chaque résultat d'outil conserve un champ `details.approvalType` (par exemple `shellJudge` : approuvée par l'analyseur déterministe)
et, selon le cas, des informations de l'étage « Shell Reviewer ». Le script ne fait qu'une LECTURE d'une copie de la base : l'application
peut rester ouverte.

Usage : python lire_approbations_bionic.py [identifiant_projet] [--brut]
Le projet par défaut est celui du dépôt fictif bionic-demo (« Démo code »).
"""
import json
import os
import shutil
import sqlite3
import sys
import tempfile
import time

PROJETS = os.path.join(os.path.expanduser("~"), ".lmstudio", "apps", "bionic", "projects")
PAR_DEFAUT = "eb1a6169-6b95-4057-9081-a0f1423091b3"   # « Démo code » (répertoire de travail : bionic-demo)


def copie_base(projet):
    src = os.path.join(PROJETS, projet, ".internal")
    tmp = tempfile.mkdtemp(prefix="bionic_ro_")
    for nom in ("ng-sessions.sqlite", "ng-sessions.sqlite-wal", "ng-sessions.sqlite-shm"):
        if os.path.exists(os.path.join(src, nom)):
            shutil.copy(os.path.join(src, nom), tmp)
    return os.path.join(tmp, "ng-sessions.sqlite")


def entrees(projet):
    con = sqlite3.connect(copie_base(projet))
    rows = con.execute("select entry_json from chat_entries").fetchall()
    out = []
    for (js,) in rows:
        try:
            out.append(json.loads(js))
        except json.JSONDecodeError:
            pass
    return sorted(out, key=lambda e: e.get("createdTimestamp", 0))


def commandes(projet, depuis=0):
    """Liste des commandes shell exécutées ou refusées : (horodatage, commande, type d'approbation, erreur, extrait de sortie, détails bruts)."""
    res = []
    for e in entrees(projet):
        if e.get("createdTimestamp", 0) < depuis:
            continue
        msg = e.get("message")
        if not isinstance(msg, dict):
            continue
        for p in msg.get("parts", []):
            if p.get("type") != "toolCallResult":
                continue
            det = p.get("details") or {}
            part = (det.get("previewContent") or {}).get("partValues") or {}
            cmd = (part.get("command") or {}).get("text")
            if cmd is None:
                continue
            txt = " ".join(x.get("text", "") for x in p.get("result", []) if isinstance(x, dict))
            res.append({"t": e["createdTimestamp"], "commande": cmd, "approbation": det.get("approvalType"), "erreur": det.get("isError"),
                        "sortie": txt[:160].replace("\n", " | "), "details": det})
    return res


if __name__ == "__main__":
    projet = next((a for a in sys.argv[1:] if not a.startswith("--")), PAR_DEFAUT)
    for c in commandes(projet):
        h = time.strftime("%H:%M:%S", time.localtime(c["t"] / 1000))
        print(f"{h}  {str(c['approbation']):14s} erreur={c['erreur']!s:5s} {c['commande'][:90]}")
        if "--brut" in sys.argv:
            print("   ", json.dumps(c["details"], ensure_ascii=False)[:600])


def resume(projet, depuis=0):
    """Outils appelés (dans l'ordre) et dernière réponse textuelle de l'agent depuis `depuis` (ms) : lecture de la base, sans passer par l'écran."""
    outils, derniere = [], ""
    for e in entrees(projet):
        if e.get("createdTimestamp", 0) < depuis:
            continue
        msg = e.get("message")
        if not isinstance(msg, dict) or msg.get("role") != "assistant":
            continue
        for p in msg.get("parts", []):
            if p.get("type") == "toolCallRequest":
                outils.append(p.get("name"))
            elif p.get("type") == "text" and not (p.get("text") or "").startswith("<name>"):
                derniere = p.get("text") or derniere
    return outils, derniere


def modele_reel(projet, depuis=0):
    """Modèle enregistré dans la base pour la session la plus récente du projet (hors sous-sessions de compaction) : vérifie le modèle réellement utilisé."""
    con = sqlite3.connect(copie_base(projet))
    for sj, ts, nom in con.execute("select session_json, updated_timestamp, session_name from sessions order by updated_timestamp desc"):
        if nom == "Compaction" or ts < depuis - 60000:
            continue
        return json.loads(sj).get("modelSpecifier", {}).get("indexedModelIdentifier")
    return None


def modeles_sessions(projet, depuis=0):
    """Liste (nom de session, modèle enregistré) de toutes les sessions du projet modifiées depuis `depuis` (ms), sous-sessions « Compaction » comprises."""
    con = sqlite3.connect(copie_base(projet))
    out = []
    for sj, ts, nom in con.execute("select session_json, updated_timestamp, session_name from sessions order by updated_timestamp desc"):
        if ts >= depuis - 60000:
            out.append((nom, json.loads(sj).get("modelSpecifier", {}).get("indexedModelIdentifier")))
    return out


def durees_sessions(projet, depuis=0):
    """Pour chaque session (hors sous-sessions) modifiée depuis `depuis` (ms) : (modèle, horodatage du premier message utilisateur, horodatage de la dernière réponse
    de l'assistant, réponse finale terminée ?). Relevé dans la base, donc indépendant de l'affichage (colonnes, onglets)."""
    con = sqlite3.connect(copie_base(projet))
    out = []
    for sid, head, sj, ts, parent in con.execute("select session_id, committed_head_entry_id, session_json, updated_timestamp, parent_session_id from sessions"):
        if parent or ts < depuis - 60000 or not head:
            continue
        chaine, cur = [], head
        while cur:
            row = con.execute("select previous_id, entry_json from chat_entries where id=?", (cur,)).fetchone()
            if not row:
                break
            chaine.append(json.loads(row[1]))
            cur = row[0]
        user = [e for e in chaine if e.get("type") == "message" and e.get("message", {}).get("role") == "user"]
        asst = [e for e in chaine if e.get("type") == "message" and e.get("message", {}).get("role") == "assistant"]
        if not user or not asst or user[-1].get("createdTimestamp", 0) < depuis:
            continue
        finale = not any(p.get("type") == "toolCallRequest" for p in asst[0]["message"].get("parts", []))
        out.append({"modele": json.loads(sj).get("modelSpecifier", {}).get("indexedModelIdentifier"), "t_utilisateur_ms": user[-1]["createdTimestamp"],
                    "t_assistant_ms": asst[0]["createdTimestamp"], "terminee": finale})
    return out
