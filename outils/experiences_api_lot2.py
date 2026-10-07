"""Expériences du lot 2 sur l'API locale de LM Studio : chat à état, /v1/responses, /v1/messages, statistiques,
sortie structurée, appel d'outils. Résultats bruts : outils/resultats/lot2_*.json.

Usage : python experiences_api_lot2.py <etat|responses|messages|stats|structure|outils> [modele]
Variables facultatives : LMSTUDIO_URL (défaut http://127.0.0.1:1234), LMSTUDIO_TOKEN (jeton d'API si l'authentification est activée).
Aucune donnée réelle ; les outils sont ceux de serveur_mcp_demo.py (jamais exécutés avec effet de bord).
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import serveur_mcp_demo as srv  # noqa: E402

BASE = os.environ.get("LMSTUDIO_URL", "http://127.0.0.1:1234")
TOKEN = os.environ.get("LMSTUDIO_TOKEN")
MODELE = sys.argv[2] if len(sys.argv) > 2 else "google/gemma-4-e4b"
SORTIE = os.path.join(ICI, "resultats")


def api(chemin, corps=None, entetes=None, flux=False, methode=None, timeout=600):
    h = {"Content-Type": "application/json"}
    if TOKEN:
        h["Authorization"] = f"Bearer {TOKEN}"
    h.update(entetes or {})
    data = json.dumps(corps).encode() if corps is not None else None
    req = urllib.request.Request(BASE + chemin, data=data, headers=h, method=methode)
    t0 = time.time()
    try:
        r = urllib.request.urlopen(req, timeout=timeout)
    except urllib.error.HTTPError as e:
        txt = e.read().decode("utf-8", "replace")
        try:
            txt = json.loads(txt)
        except json.JSONDecodeError:
            pass
        return e.code, dict(e.headers), txt, round(time.time() - t0, 2)
    if flux:
        evts = []
        for brut in r:
            ligne = brut.decode("utf-8").strip()
            if ligne.startswith("event:"):
                evts.append({"event": ligne[6:].strip()})
            elif ligne.startswith("data:"):
                d = ligne[5:].strip()
                if d == "[DONE]":
                    evts.append({"data": "[DONE]"})
                    continue
                try:
                    obj = json.loads(d)
                except json.JSONDecodeError:
                    obj = d
                if evts and "event" in evts[-1] and "data" not in evts[-1]:
                    evts[-1]["data"] = obj
                else:
                    evts.append({"data": obj})
        return r.status, dict(r.headers), evts, round(time.time() - t0, 2)
    return r.status, dict(r.headers), json.load(r), round(time.time() - t0, 2)


def sauver(nom, data):
    with open(os.path.join(SORTIE, f"lot2_{nom}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("-> enregistré :", nom, flush=True)


def texte_sortie(o):
    """Texte des éléments « message » d'une sortie /api/v1/chat."""
    return " ".join(i.get("content", "") for i in o.get("output", []) if i.get("type") == "message")


def court(x, n=400):
    s = json.dumps(x, ensure_ascii=False)
    return s if len(s) <= n else s[:n] + "…"


OUTILS_OPENAI = [{"type": "function", "function": {"name": o["name"], "description": o["description"], "parameters": o["inputSchema"]}}
                 for o in srv.OUTILS]


# --------------------------------------------------------------------------------------------------------------------
def etat():
    res = {}
    base = {"model": MODELE, "reasoning": "off", "temperature": 0, "max_output_tokens": 60}
    s, h, o1, t = api("/api/v1/chat", dict(base, input="Retiens ce code : ZEBRE-42. Réponds seulement : noté."))
    res["tour1"] = {"status": s, "secondes": t, "reponse": texte_sortie(o1), "stats": o1.get("stats"), "response_id": o1.get("response_id"),
                    "cles": sorted(o1.keys())}
    r1 = o1.get("response_id")
    s, h, o2, t = api("/api/v1/chat", dict(base, input="Quel est le code que je t'ai demandé de retenir ?", previous_response_id=r1))
    res["tour2_avec_id"] = {"status": s, "reponse": texte_sortie(o2), "stats": o2.get("stats"), "response_id": o2.get("response_id")}
    r2 = o2.get("response_id")
    s, h, o3, t = api("/api/v1/chat", dict(base, input="Répète le code en minuscules.", previous_response_id=r1))
    res["branche_depuis_tour1"] = {"status": s, "reponse": texte_sortie(o3), "stats": o3.get("stats"), "response_id": o3.get("response_id")}
    s, h, o4, t = api("/api/v1/chat", dict(base, input="Quelle était ma toute première question ?", previous_response_id=r2))
    res["tour3_apres_tour2"] = {"status": s, "reponse": texte_sortie(o4), "stats": o4.get("stats")}
    s, h, o5, t = api("/api/v1/chat", dict(base, input="Quel est le code que je t'ai demandé de retenir ?"))
    res["sans_previous_response_id"] = {"status": s, "reponse": texte_sortie(o5), "stats": o5.get("stats")}
    s, h, o6, t = api("/api/v1/chat", dict(base, input="Dis seulement : bonjour.", store=False))
    res["store_false"] = {"status": s, "reponse": texte_sortie(o6), "response_id_present": "response_id" in o6}
    s, h, o7, t = api("/api/v1/chat", dict(base, input="suite", previous_response_id="resp_inexistant"))
    res["id_inconnu"] = {"status": s, "corps": o7}
    for k, v in res.items():
        print(k, court(v, 300))
    sauver("etat", res)


def responses():
    res = {}
    base = {"model": MODELE, "max_output_tokens": 80, "temperature": 0, "reasoning": {"effort": "none"}}
    s, h, o, t = api("/v1/responses", dict(base, input="Retiens ce code : ZEBRE-42. Réponds seulement : noté.", instructions="Réponds en français, très brièvement."))
    res["tour1"] = {"status": s, "cles": sorted(o.keys()) if isinstance(o, dict) else o, "id": o.get("id"), "usage": o.get("usage"),
                    "output": o.get("output"), "store": o.get("store"), "instructions": o.get("instructions")}
    rid = o.get("id")
    s, h, o2, t = api("/v1/responses", dict(base, input="Quel est le code ?", previous_response_id=rid))
    res["tour2_previous_response_id"] = {"status": s, "output": o2.get("output"), "usage": o2.get("usage"), "previous_response_id": o2.get("previous_response_id")}
    s, h, ev, t = api("/v1/responses", dict(base, input="Compte de 1 à 3.", stream=True), flux=True)
    res["flux"] = {"status": s, "secondes": t, "types": [e.get("event") or (e.get("data") or {}).get("type") for e in ev][:40]}
    s, h, o3, t = api("/v1/responses", dict(base, input="Convertis 100 degrés Celsius en Fahrenheit.",
                                              tools=[{"type": "function", "name": x["name"], "description": x["description"], "parameters": x["inputSchema"]} for x in srv.OUTILS],
                                              max_output_tokens=300))
    res["outil"] = {"status": s, "output": o3.get("output") if isinstance(o3, dict) else o3}
    appels = [i for i in (o3.get("output") or []) if i.get("type") == "function_call"] if isinstance(o3, dict) else []
    if appels:
        a = appels[0]
        sortie = srv.FONCTIONS[a["name"]](**json.loads(a["arguments"]))
        s, h, o4, t = api("/v1/responses", dict(base, previous_response_id=o3["id"],
                                                  input=[{"type": "function_call_output", "call_id": a["call_id"], "output": sortie}], max_output_tokens=200))
        res["outil_retour"] = {"status": s, "resultat_outil": sortie, "output": o4.get("output") if isinstance(o4, dict) else o4}
    schema = {"type": "object", "properties": {"pays": {"type": "string"}, "capitale": {"type": "string"}}, "required": ["pays", "capitale"], "additionalProperties": False}
    s, h, o5, t = api("/v1/responses", dict(base, input="Donne un pays européen et sa capitale.",
                                              text={"format": {"type": "json_schema", "name": "pays", "schema": schema, "strict": True}}))
    res["sortie_structuree"] = {"status": s, "output": o5.get("output") if isinstance(o5, dict) else o5}
    for k, v in res.items():
        print(k, court(v, 350))
    sauver("responses", res)


def messages():
    res = {}
    base = {"model": MODELE, "max_tokens": 200, "temperature": 0}
    s, h, o, t = api("/v1/messages", dict(base, system="Réponds en français, en une phrase.",
                                           messages=[{"role": "user", "content": "Mon prénom est Camille."}, {"role": "assistant", "content": "Bonjour Camille."},
                                                     {"role": "user", "content": "Quel est mon prénom ?"}]))
    res["multi_tours"] = {"status": s, "reponse": o}
    s, h, ev, t = api("/v1/messages", dict(base, stream=True, messages=[{"role": "user", "content": "Compte de 1 à 3."}]), flux=True)
    res["flux"] = {"status": s, "types": [e.get("event") for e in ev][:30], "premiers": ev[:3]}
    outils = [{"name": x["name"], "description": x["description"], "input_schema": x["inputSchema"]} for x in srv.OUTILS]
    s, h, o2, t = api("/v1/messages", dict(base, max_tokens=300, tools=outils, messages=[{"role": "user", "content": "Convertis 100 degrés Celsius en Fahrenheit."}]))
    res["outil"] = {"status": s, "reponse": o2}
    blocs = [b for b in (o2.get("content") or []) if b.get("type") == "tool_use"] if isinstance(o2, dict) else []
    if blocs:
        b = blocs[0]
        sortie = srv.FONCTIONS[b["name"]](**b["input"])
        s, h, o3, t = api("/v1/messages", dict(base, max_tokens=300, tools=outils, messages=[
            {"role": "user", "content": "Convertis 100 degrés Celsius en Fahrenheit."},
            {"role": "assistant", "content": o2["content"]},
            {"role": "user", "content": [{"type": "tool_result", "tool_use_id": b["id"], "content": sortie}]}]))
        res["outil_retour"] = {"status": s, "resultat_outil": sortie, "reponse": o3}
        # variantes du second appel : l'absence de texte final après un tool_result seul est un défaut constaté avec Gemma 4 E4B
        base_msgs = [{"role": "user", "content": "Convertis 100 degrés Celsius en Fahrenheit."}, {"role": "assistant", "content": o2["content"]}]
        retour = {"type": "tool_result", "tool_use_id": b["id"], "content": sortie}
        variantes = {
            "tools_declares_tool_result_seul": dict(tools=outils, messages=base_msgs + [{"role": "user", "content": [retour]}]),
            "tools_omis": dict(messages=base_msgs + [{"role": "user", "content": [retour]}]),
            "tool_result_plus_texte": dict(tools=outils, messages=base_msgs + [{"role": "user", "content": [retour, {"type": "text", "text": "Donne la réponse finale."}]}]),
        }
        res["outil_retour_variantes"] = {}
        for nom, v in variantes.items():
            for i in range(3):
                s, h, ov, t = api("/v1/messages", dict({"model": MODELE, "max_tokens": 400, "temperature": 0.3}, **v))
                res["outil_retour_variantes"].setdefault(nom, []).append({"tokens_sortie": ov["usage"]["output_tokens"], "texte": (ov["content"][0]["text"][:80] if ov.get("content") else "")})
    s, h, o4, t = api("/v1/messages", dict(base, messages=[{"role": "user", "content": "Dis ok."}]), entetes={"x-api-key": "factice", "anthropic-version": "2023-06-01"})
    res["entetes_anthropic"] = {"status": s, "reponse": court(o4, 200)}
    s, h, o5, t = api("/v1/messages", {"model": MODELE, "messages": [{"role": "user", "content": "Dis ok."}]})
    res["sans_max_tokens"] = {"status": s, "reponse": court(o5, 300)}
    for k, v in res.items():
        print(k, court(v, 350))
    sauver("messages", res)


def stats():
    res = {}
    consigne = "Explique en trois phrases ce qu'est un jeton (token) pour un modèle de langage."
    s, h, o, t = api("/api/v1/chat", {"model": MODELE, "input": consigne, "reasoning": "off", "temperature": 0, "max_output_tokens": 200, "store": False})
    res["api_v1_chat"] = {"secondes_client": t, "stats": o.get("stats"), "cles": sorted(o.keys())}
    s, h, o2, t2 = api("/v1/chat/completions", {"model": MODELE, "messages": [{"role": "user", "content": consigne}], "temperature": 0, "max_tokens": 200, "reasoning_effort": "none"})
    res["openai_chat_completions"] = {"secondes_client": t2, "usage": o2.get("usage"), "cles": sorted(o2.keys()), "stats": o2.get("stats"), "timings": o2.get("timings")}
    s, h, ev, t3 = api("/api/v1/chat", {"model": MODELE, "input": consigne, "reasoning": "off", "temperature": 0, "max_output_tokens": 200, "store": False, "stream": True}, flux=True)
    res["flux_api_v1_chat"] = {"secondes_client": t3, "types": [e.get("event") or (e.get("data") or {}).get("type") for e in ev],
                               "chat_end": [e for e in ev if (e.get("event") == "chat.end" or (e.get("data") or {}).get("type") == "chat.end")][-1:]}
    for k, v in res.items():
        print(k, court(v, 500))
    sauver("stats", res)


def structure():
    schema = {"type": "object", "properties": {
        "titre": {"type": "string"}, "annee": {"type": "integer"}, "genre": {"type": "string", "enum": ["drame", "comedie", "documentaire"]},
        "acteurs": {"type": "array", "items": {"type": "string"}, "minItems": 2}}, "required": ["titre", "annee", "genre", "acteurs"], "additionalProperties": False}
    corps = {"model": MODELE, "messages": [{"role": "user", "content": "Extrais la fiche du film : « Les Ombres du Nord, un drame de 2019, avec Léa Martin et Paul Roche. »"}],
             "temperature": 0.7, "max_tokens": 1500,
             "reasoning_effort": "none", "response_format": {"type": "json_schema", "json_schema": {"name": "fiche_film", "strict": True, "schema": schema}}}
    ok, essais = 0, []
    for i in range(10):
        s, h, o, t = api("/v1/chat/completions", corps)
        c = o["choices"][0]
        try:
            d = json.loads(c["message"]["content"])
            valide = (set(d) == set(schema["required"]) and isinstance(d["annee"], int) and d["genre"] in schema["properties"]["genre"]["enum"]
                      and isinstance(d["acteurs"], list) and len(d["acteurs"]) >= 2)
        except Exception:
            d, valide = c["message"]["content"][:100], False
        ok += valide
        essais.append({"valide": valide, "secondes": t, "finish": c["finish_reason"], "contenu": d,
                       "tokens_reflexion": o["usage"].get("completion_tokens_details", {}).get("reasoning_tokens"), "tokens": o["usage"]["completion_tokens"]})
    res = {"modele": MODELE, "valides": ok, "essais": essais}
    # consigne créative : le modèle réfléchit malgré reasoning_effort = none
    s, h, o, t = api("/v1/chat/completions", dict(corps, messages=[{"role": "user", "content": "Invente la fiche d'un film fictif."}], max_tokens=2500))
    res["creatif"] = {"secondes": t, "tokens": o["usage"]["completion_tokens"], "tokens_reflexion": o["usage"].get("completion_tokens_details", {}).get("reasoning_tokens"), "finish": o["choices"][0]["finish_reason"]}
    # troncature
    c2 = dict(corps, max_tokens=12)
    s, h, o, t = api("/v1/chat/completions", c2)
    res["tronque"] = {"finish": o["choices"][0]["finish_reason"], "contenu": o["choices"][0]["message"]["content"]}
    # json_object
    s, h, o, t = api("/v1/chat/completions", {"model": MODELE, "messages": [{"role": "user", "content": "Donne un objet JSON avec une clé 'a'."}],
                                              "response_format": {"type": "json_object"}, "max_tokens": 100, "reasoning_effort": "none"})
    res["json_object"] = {"status": s, "corps": court(o, 300)}
    print(court({k: v for k, v in res.items() if k != "essais"}, 800))
    sauver("structure_" + MODELE.replace("/", "_"), res)


def outils():
    res = {}
    msgs = [{"role": "user", "content": "Convertis 0 degré Celsius en Fahrenheit, puis 100 degrés Celsius en Kelvin."}]
    base = {"model": MODELE, "tools": OUTILS_OPENAI, "temperature": 0, "max_tokens": 400, "reasoning_effort": "none"}
    # appels parallèles
    s, h, o, t = api("/v1/chat/completions", dict(base, messages=msgs))
    m = o["choices"][0]["message"]
    res["parallele"] = {"finish": o["choices"][0]["finish_reason"], "appels": [(c["function"]["name"], c["function"]["arguments"]) for c in m.get("tool_calls", [])]}
    # boucle complète
    messages_ = list(msgs) + [m]
    for c in m.get("tool_calls", []):
        sortie = srv.FONCTIONS[c["function"]["name"]](**json.loads(c["function"]["arguments"]))
        messages_.append({"role": "tool", "tool_call_id": c["id"], "content": sortie})
    s, h, o2, t = api("/v1/chat/completions", dict(base, messages=messages_))
    res["boucle_finale"] = {"finish": o2["choices"][0]["finish_reason"], "reponse": o2["choices"][0]["message"]["content"], "usage": o2["usage"]}
    # tool_choice
    q = [{"role": "user", "content": "Quelle est la capitale de l'Italie ?"}]
    for tc in ("auto", "none", "required", {"type": "function", "function": {"name": "lister_notes"}}):
        s, h, o3, t = api("/v1/chat/completions", dict(base, messages=q, tool_choice=tc))
        if s != 200:
            res[f"tool_choice_{json.dumps(tc)[:30]}"] = {"status": s, "corps": court(o3, 300)}
            continue
        c = o3["choices"][0]
        res[f"tool_choice_{json.dumps(tc)[:30]}"] = {"finish": c["finish_reason"], "appels": [x["function"]["name"] for x in c["message"].get("tool_calls", [])],
                                                      "texte": (c["message"].get("content") or "")[:80]}
    # flux
    s, h, ev, t = api("/v1/chat/completions", dict(base, messages=[{"role": "user", "content": "Convertis 100 degrés Celsius en Fahrenheit."}], stream=True), flux=True)
    deltas = [e["data"]["choices"][0]["delta"] for e in ev if isinstance(e.get("data"), dict) and e["data"].get("choices")]
    res["flux_tool_calls"] = {"morceaux": len(deltas), "avec_tool_calls": sum(1 for d in deltas if d.get("tool_calls")),
                              "exemple": [d for d in deltas if d.get("tool_calls")][:3]}
    for k, v in res.items():
        print(k, court(v, 400))
    sauver("outils_api_" + MODELE.replace("/", "_"), res)


def raisonnement():
    """Effet du champ reasoning de /api/v1/chat (off, low, medium, high, on) sur le nombre de tokens de réflexion et la durée."""
    res = {}
    for niveau in ("off", "low", "medium", "high", "on"):
        s, h, o, t = api("/api/v1/chat", {"model": MODELE, "input": "Combien font 17 × 23 ? Réponds par le nombre seul.", "reasoning": niveau,
                                           "temperature": 0, "max_output_tokens": 1500, "store": False})
        if s != 200:
            res[niveau] = {"status": s, "corps": o}
        else:
            res[niveau] = {"secondes": t, "reflexion_tokens": o["stats"]["reasoning_output_tokens"], "sortie_tokens": o["stats"]["total_output_tokens"],
                           "reponse": texte_sortie(o)[:40], "types": [i["type"] for i in o["output"]]}
        print(niveau, res[niveau], flush=True)
    sauver("raisonnement", res)


def system_prompt_et_contexte():
    res = {}
    s, h, o, t = api("/api/v1/chat", {"model": MODELE, "input": "Que fais-tu ?", "system_prompt": "Tu es un correcteur d'orthographe. Réponds en une phrase.",
                                       "reasoning": "off", "temperature": 0, "max_output_tokens": 80, "store": False})
    res["system_prompt"] = {"status": s, "reponse": texte_sortie(o) if s == 200 else o}
    s, h, o, t = api("/api/v1/chat", {"model": MODELE, "input": "Dis ok.", "reasoning": "off", "context_length": 2048, "max_output_tokens": 10, "store": False})
    res["context_length_2048_sur_modele_charge_16384"] = {"status": s, "corps": o if s != 200 else {"stats": o["stats"], "reponse": texte_sortie(o)}}
    s, h, o, t = api("/api/v1/chat", {"model": MODELE, "input": "Dis ok.", "reasoning": "off", "min_p": 0.05, "top_k": 40, "repeat_penalty": 1.1, "top_p": 0.9, "max_output_tokens": 10, "store": False})
    res["parametres_echantillonnage"] = {"status": s, "reponse": texte_sortie(o) if s == 200 else o}
    s, h, o, t = api("/api/v1/chat", {"model": MODELE, "input": "Dis ok.", "reasoning": "off", "max_output_tokens": 10, "store": False, "parametre_inconnu": 1})
    res["parametre_inconnu"] = {"status": s, "corps": o if s != 200 else "accepté"}
    for k, v in res.items():
        print(k, court(v, 300))
    sauver("chat_options", res)


if __name__ == "__main__":
    {"etat": etat, "responses": responses, "messages": messages, "stats": stats, "structure": structure, "outils": outils, "raisonnement": raisonnement, "options": system_prompt_et_contexte}[sys.argv[1]]()
