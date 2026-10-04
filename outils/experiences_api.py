"""Mesures réalisées sur le poste de test via l'API locale de LM Studio (http://127.0.0.1:1234).
Les résultats bruts sont écrits dans outils/resultats/*.json et servent de base aux chiffres cités dans les manuels.
Aucune donnée réelle : les images de test sont générées (document fictif).
"""
import base64, io, json, os, sys, time, urllib.request, urllib.error

BASE = "http://127.0.0.1:1234"
MODEL = "google/gemma-4-e4b"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultats")
os.makedirs(OUT, exist_ok=True)
NOTHINK = {"reasoning_effort": "none"}


def post(path, body, timeout=900):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            out = json.load(r)
    except urllib.error.HTTPError as e:
        return {"HTTP_ERROR": e.code, "body": e.read().decode()[:800]}, time.time() - t0
    return out, time.time() - t0


def chat(messages, **params):
    body = {"model": MODEL, "messages": messages}
    body.update(params)
    o, dt = post("/v1/chat/completions", body)
    if "choices" not in o:
        return {"error": o, "seconds": round(dt, 2)}
    c = o["choices"][0]
    u = o["usage"]
    return {"content": c["message"]["content"], "reasoning": c["message"].get("reasoning_content", ""),
            "finish": c["finish_reason"], "prompt_tokens": u["prompt_tokens"], "completion_tokens": u["completion_tokens"],
            "seconds": round(dt, 2), "tok_s_global": round(u["completion_tokens"] / dt, 2) if dt else None}


def save(name, data):
    with open(os.path.join(OUT, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("saved", name, flush=True)


def make_images():
    from PIL import Image, ImageDraw, ImageFont
    def font(sz, bold=False):
        return ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf", sz)
    # 1. facture fictive 1288 px (grand côté)
    W, H = 910, 1288
    img = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(img)
    d.text((50, 50), "SOCIÉTÉ EXEMPLE SAS", font=font(34, True), fill="black")
    d.text((50, 95), "12 rue des Tests, 75000 Paris - SIRET 123 456 789 00012", font=font(18), fill="black")
    d.text((50, 160), "FACTURE N° F-2026-0042", font=font(30, True), fill="black")
    d.text((50, 205), "Date : 06/10/2026          Échéance : 05/11/2026", font=font(20), fill="black")
    d.text((50, 260), "Client : Atelier Démo SARL", font=font(20), fill="black")
    rows = [("Désignation", "Qté", "PU HT", "Total HT"),
            ("Audit de configuration", "2", "450,00 €", "900,00 €"),
            ("Formation prise en main", "1", "1 200,00 €", "1 200,00 €"),
            ("Support mensuel", "3", "150,00 €", "450,00 €")]
    y = 340
    xs = [50, 520, 610, 740]
    for i, r in enumerate(rows):
        for x, t in zip(xs, r):
            d.text((x, y), t, font=font(20, i == 0), fill="black")
        d.line((50, y + 34, 860, y + 34), fill="black", width=2 if i == 0 else 1)
        y += 48
    d.text((560, y + 30), "Total HT : 2 550,00 €", font=font(22), fill="black")
    d.text((560, y + 68), "TVA 20 % : 510,00 €", font=font(22), fill="black")
    d.text((560, y + 106), "Total TTC : 3 060,00 €", font=font(26, True), fill="black")
    d.text((50, H - 90), "Paiement par virement sous 30 jours. Pénalités de retard : 3 fois le taux légal.", font=font(15), fill="black")
    p = os.path.join(OUT, "facture_test_1288.png"); img.save(p)
    small = img.resize((int(W * 640 / H), 640)); small.save(os.path.join(OUT, "facture_test_640.png"))
    return p


def b64(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def e1_temperature():
    prompt = "Écris en deux phrases le début d'une histoire sur un ingénieur qui découvre une anomalie dans une salle de contrôle."
    res = {}
    for T in [0, 0.5, 1.0, 1.5]:
        runs = [chat([{"role": "user", "content": prompt}], temperature=T, max_tokens=90, **NOTHINK) for _ in range(3)]
        res[str(T)] = {"distinct": len(set(r["content"] for r in runs)), "contents": [r["content"] for r in runs],
                       "tok_s": [r["tok_s_global"] for r in runs]}
        print("E1 T=", T, "distincts:", res[str(T)]["distinct"], flush=True)
    save("e1_temperature", res)


def e2_stop_length():
    res = {}
    res["max_tokens=15"] = chat([{"role": "user", "content": "Décris le fonctionnement d'une turbine à vapeur."}], max_tokens=15, temperature=0, **NOTHINK)
    res["stop=['2.']"] = chat([{"role": "user", "content": "Liste 5 conseils pour bien écrire un rapport technique, numérotés 1. 2. 3. etc."}], stop=["2."], temperature=0, max_tokens=200, **NOTHINK)
    res["seed_repeat"] = [chat([{"role": "user", "content": "Donne un nom original pour un robot ménager."}], temperature=1.0, seed=42, max_tokens=20, **NOTHINK)["content"] for _ in range(3)]
    save("e2_stop_length_seed", res)
    print("E2 done", flush=True)


def e3_structured():
    schema = {"type": "json_schema", "json_schema": {"name": "facture", "strict": True, "schema": {
        "type": "object", "properties": {
            "numero": {"type": "string"}, "date": {"type": "string"}, "client": {"type": "string"},
            "total_ttc": {"type": "number"}},
        "required": ["numero", "date", "client", "total_ttc"], "additionalProperties": False}}}
    txt = "Facture F-2026-0042 du 06/10/2026 pour Atelier Démo SARL. Total TTC : 3 060,00 euros."
    r = chat([{"role": "user", "content": "Extrais les informations de ce texte : " + txt}], response_format=schema, temperature=0, max_tokens=300, **NOTHINK)
    try:
        r["parsed"] = json.loads(r["content"])
    except Exception as e:
        r["parsed_error"] = str(e)
    save("e3_structured", r)
    print("E3", r.get("parsed"), flush=True)


def e4_embeddings():
    o, dt = post("/v1/embeddings", {"model": "text-embedding-nomic-embed-text-v1.5",
                                    "input": ["La centrale produit de l'électricité.", "Une usine génère du courant électrique.", "Le chat dort sur le canapé."]})
    if "data" not in o:
        save("e4_embeddings", o); print("E4 erreur", o); return
    v = [d["embedding"] for d in o["data"]]
    import math
    cos = lambda a, b: sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))
    res = {"dim": len(v[0]), "seconds_incl_load": round(dt, 2), "cos_1_2": round(cos(v[0], v[1]), 3), "cos_1_3": round(cos(v[0], v[2]), 3)}
    save("e4_embeddings", res); print("E4", res, flush=True)


def e5_stream():
    body = {"model": MODEL, "messages": [{"role": "user", "content": "Compte de 1 à 20 en français, séparés par des virgules."}],
            "stream": True, "temperature": 0, "max_tokens": 120, **NOTHINK}
    req = urllib.request.Request(BASE + "/v1/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    t0 = time.time(); first = None; n = 0; text = ""
    with urllib.request.urlopen(req, timeout=300) as r:
        for line in r:
            line = line.decode().strip()
            if not line.startswith("data:") or line.endswith("[DONE]"):
                continue
            ch = json.loads(line[5:])
            delta = ch["choices"][0]["delta"].get("content") if ch.get("choices") else None
            if delta:
                if first is None:
                    first = time.time() - t0
                n += 1; text += delta
    res = {"ttft_s": round(first, 2) if first else None, "total_s": round(time.time() - t0, 2), "chunks": n, "text": text}
    save("e5_stream", res); print("E5", res, flush=True)


def e6_tools():
    tools = [{"type": "function", "function": {"name": "get_meteo", "description": "Donne la météo d'une ville",
              "parameters": {"type": "object", "properties": {"ville": {"type": "string"}}, "required": ["ville"]}}}]
    o, dt = post("/v1/chat/completions", {"model": MODEL, "messages": [{"role": "user", "content": "Quel temps fait-il à Lyon ?"}],
                                          "tools": tools, "temperature": 0, "max_tokens": 300, **NOTHINK})
    save("e6_tools", o); print("E6", json.dumps(o.get("choices", [{}])[0].get("message", o))[:400], flush=True)


def e7_vision(img1288):
    prompt = ("Transcris fidèlement tout le texte de ce document en Markdown (conserve le tableau). "
              "Ne rajoute aucun commentaire.")
    res = {}
    for label, path in [("1288px", img1288), ("640px", os.path.join(OUT, "facture_test_640.png"))]:
        r = chat([{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": b64(path)}}]}],
                 temperature=0, max_tokens=700, **NOTHINK)
        res[label] = r
        print("E7", label, r.get("seconds"), "s", "prompt_tokens", r.get("prompt_tokens"), "compl", r.get("completion_tokens"), flush=True)
    save("e7_vision_ocr", res)


def e8_prompt_speed():
    filler = ("La production d'électricité repose sur un ensemble de procédés industriels complexes. " * 140)
    r = chat([{"role": "user", "content": filler + "\n\nRésume ce texte en une phrase."}], temperature=0, max_tokens=40, **NOTHINK)
    save("e8_prompt_speed", r); print("E8", {k: r.get(k) for k in ("prompt_tokens", "completion_tokens", "seconds")}, flush=True)


if __name__ == "__main__":
    which = sys.argv[1:] or ["e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8"]
    img = make_images()
    # échauffement
    chat([{"role": "user", "content": "ok"}], max_tokens=3, **NOTHINK)
    for w in which:
        {"e1": e1_temperature, "e2": e2_stop_length, "e3": e3_structured, "e4": e4_embeddings, "e5": e5_stream,
         "e6": e6_tools, "e7": lambda: e7_vision(img), "e8": e8_prompt_speed}[w]()
