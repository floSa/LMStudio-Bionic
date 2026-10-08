"""Protocole de validation d'OlmOCR 2 7B (Manuel 05, section 7.8) avec les fichiers déjà présents sur le disque :
OlmOCR 2 7B en Q4_K_M et en Q8_0, comparés à Gemma 4 E4B (Q8_0). Aucune donnée réelle : les pages sont générées (fictives).

Pages : (1) texte anglais, (2) facture française à tableau (accents), (3) tableau dense de chiffres, (4) la facture tournée de 90°.
Mesures : mémoire (VRAM, RAM), durée, jetons d'entrée et de sortie, vitesse ; exactitude = part des éléments attendus retrouvés dans la sortie.
Résultats : outils/resultats/gpu_dedie/olmocr_protocole.json et pages de test dans outils/resultats/gpu_dedie/pages_ocr/.

Usage : python essai_olmocr.py
"""
import base64
import io
import json
import os
import re
import sys
import time

from PIL import Image, ImageDraw, ImageFont

import subprocess

from gpu_bench import Ligne, api, decharger, memoire_apres, sauver, serialiser

ICI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ICI, "resultats", "gpu_dedie")
PAGES = os.path.join(OUT, "pages_ocr")
os.makedirs(PAGES, exist_ok=True)

PROMPT_OLMOCR = (
    "Attached is one page of a document that you must process. Just return the plain text representation of this document "
    "as if you were reading it naturally. Convert equations to LateX and tables to HTML.\n"
    "If there are any figures or charts, label them with the following markdown syntax "
    "![Alt text describing the contents of the figure](page_startx_starty_width_height.png)\n"
    "Return your output as markdown, with a front matter section on top specifying values for the primary_language, "
    "is_rotation_valid, rotation_correction, is_table, and is_diagram parameters."
)
PROMPT_GEMMA = "Transcris fidèlement tout le texte de ce document en Markdown (conserve les tableaux). Ne rajoute aucun commentaire."


def police(taille, gras=False):
    return ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf" if gras else r"C:\Windows\Fonts\arial.ttf", taille)


def page_anglaise():
    img = Image.new("RGB", (910, 1288), "white")
    d = ImageDraw.Draw(img)
    d.text((60, 60), "Quarterly Maintenance Report", font=police(36, True), fill="black")
    lignes = ["The cooling system of Unit 3 was inspected on 12 September 2026.",
              "Two pumps showed a pressure drop of 8 percent compared with",
              "the previous quarter. The valves V-114 and V-208 were replaced.",
              "", "Findings:", "1. Pump P-2 vibration level: 4.7 mm/s (limit 7.1 mm/s).",
              "2. Filter F-17 clogging rate: 62 percent.", "3. Total downtime: 14 hours.",
              "", "Recommendation: schedule a full overhaul before March 2027."]
    y = 140
    for l in lignes:
        d.text((60, y), l, font=police(23), fill="black")
        y += 44
    img.save(os.path.join(PAGES, "p1_anglais.png"))
    return ["Quarterly Maintenance Report", "12 September 2026", "8 percent", "V-114", "V-208", "P-2", "4.7 mm/s", "7.1 mm/s", "F-17", "62 percent", "14 hours", "March 2027"]


def page_tableau_dense():
    img = Image.new("RGB", (910, 1288), "white")
    d = ImageDraw.Draw(img)
    d.text((50, 50), "Budget prévisionnel 2027 — répartition par service", font=police(28, True), fill="black")
    entetes = ["Service", "T1", "T2", "T3", "T4", "Total"]
    lignes = [["Maintenance", "12 450", "13 120", "11 980", "14 300", "51 850"],
              ["Exploitation", "28 900", "29 410", "30 275", "31 040", "119 625"],
              ["Sécurité", "7 215", "7 215", "7 640", "8 120", "30 190"],
              ["Formation", "3 480", "5 960", "2 750", "6 410", "18 600"],
              ["Qualité", "4 105", "4 105", "4 390", "4 390", "16 990"],
              ["Informatique", "9 860", "10 345", "9 120", "12 770", "42 095"],
              ["Logistique", "15 330", "14 870", "16 245", "17 905", "64 350"],
              ["Achats", "2 640", "2 815", "3 090", "3 255", "11 800"]]
    xs = [50, 330, 440, 550, 660, 770]
    y = 130
    for i, r in enumerate([entetes] + lignes):
        for x, t in zip(xs, r):
            d.text((x, y), t, font=police(21, i == 0), fill="black")
        d.line((50, y + 34, 860, y + 34), fill="black", width=2 if i == 0 else 1)
        y += 48
    img.save(os.path.join(PAGES, "p3_tableau_dense.png"))
    return [c for r in lignes for c in r if re.search(r"\d", c)] + ["Maintenance", "Sécurité", "Informatique"]


def preparer():
    attendu = {}
    attendu["p1_anglais.png"] = page_anglaise()
    attendu["p3_tableau_dense.png"] = page_tableau_dense()
    fact = Image.open(os.path.join(ICI, "resultats", "facture_test_1288.png")).convert("RGB")
    fact.save(os.path.join(PAGES, "p2_facture.png"))
    attendu["p2_facture.png"] = ["F-2026-0042", "06/10/2026", "Atelier Démo SARL", "Audit de configuration", "Formation prise en main", "Support mensuel",
                                 "2 550,00", "510,00", "3 060,00", "1 200,00", "450,00", "900,00"]
    fact.rotate(-90, expand=True).save(os.path.join(PAGES, "p4_facture_tournee.png"))
    attendu["p4_facture_tournee.png"] = attendu["p2_facture.png"]
    return attendu


def normaliser(s):
    s = s.replace("\u202f", " ").replace("\xa0", " ").replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", s).lower()


def exactitude(sortie, attendus):
    n = normaliser(sortie)
    trouves = [a for a in attendus if normaliser(a) in n]
    return round(len(trouves) / len(attendus), 3), [a for a in attendus if a not in trouves]


def charger_sdk(cle):
    """`lms load` ne retrouve pas la variante Q8_0 d'OlmOCR (« Model not found ») alors que le SDK la charge : chargement par sdk_js/charger.mjs."""
    base = Ligne()
    cfg = {"contextLength": 16384, "gpu": {"ratio": "max"}, "maxParallelPredictions": 1}
    t0 = time.time()
    r = subprocess.run(["node", "charger.mjs", cle, "ocr", json.dumps(cfg)], cwd=os.path.join(ICI, "sdk_js"), capture_output=True, text=True, encoding="utf-8", timeout=600)
    ok = '"ok":true' in r.stdout
    return {"ok": ok, "load_s": round(time.time() - t0, 1), "sortie": (r.stdout + r.stderr)[-200:], "base": base}


def requete(modele, prompt, png, ordre_texte_image=True, sans_reflexion=False):
    b64 = "data:image/png;base64," + base64.b64encode(open(png, "rb").read()).decode()
    contenu = [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": b64}}]
    if not ordre_texte_image:
        contenu.reverse()
    t0 = time.time()
    code, rep = api("/v1/chat/completions", {"model": modele, "messages": [{"role": "user", "content": contenu}], "temperature": 0.1,
                                                "max_tokens": 8000, **({"reasoning_effort": "none"} if sans_reflexion else {})})
    dt = time.time() - t0
    if code != 200:
        return {"erreur": str(rep)[:300], "secondes": round(dt, 2)}
    u = rep["usage"]
    return {"secondes": round(dt, 2), "jetons_entree": u["prompt_tokens"], "jetons_sortie": u["completion_tokens"],
            "tok_s_global": round(u["completion_tokens"] / dt, 1), "finish": rep["choices"][0]["finish_reason"],
            "sortie": rep["choices"][0]["message"]["content"]}


if __name__ == "__main__":
    attendu = preparer()
    CAS = [("OlmOCR 2 7B Q4_K_M", "olmocr-2-7b-1025@q4_k_m", PROMPT_OLMOCR, True),
           ("OlmOCR 2 7B Q8_0", "olmocr-2-7b-1025@q8_0", PROMPT_OLMOCR, True),
           ("Gemma 4 E4B Q8_0", "google/gemma-4-e4b", PROMPT_GEMMA, False)]
    resultats = []
    for nom, cle, prompt, _ in CAS:
        decharger()
        ch = charger_sdk(cle)
        ligne = {"modele": nom, **serialiser(ch), "pages": {}}
        if ch["ok"]:
            ligne["memoire"] = memoire_apres(ch["base"])
            sr = "gemma" in cle
            requete("ocr", prompt, os.path.join(PAGES, "p2_facture.png"), sans_reflexion=sr)  # échauffement (non compté)
            for page, att in attendu.items():
                r = requete("ocr", prompt, os.path.join(PAGES, page), sans_reflexion=sr)
                if "sortie" in r:
                    r["exactitude"], r["manquants"] = exactitude(r["sortie"], att)
                    r["entete_yaml"] = bool(re.match(r"^\s*---\s*\n.*?\n---", r["sortie"], re.S))
                    m = re.search(r"rotation_correction:\s*(-?\d+)", r["sortie"])
                    r["rotation_correction"] = int(m.group(1)) if m else None
                ligne["pages"][page] = r
                print(nom, page, {k: v for k, v in r.items() if k not in ("sortie", "manquants")}, "manquants:", r.get("manquants"), flush=True)
        resultats.append(ligne)
        sauver("gpu_dedie/olmocr_protocole.json", resultats)
    decharger()
    print("terminé")
