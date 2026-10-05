"""OCR par lot : envoie chaque image de page d'un dossier à un modèle de vision servi par LM Studio et écrit un .md par page.

Pensé pour OlmOCR 2 7B (prompt officiel, température 0.1, 8000 tokens max, en-tête YAML) mais utilisable avec un autre modèle
de vision (ex. Gemma 4 E4B : ajouter --sans-yaml et --modele google/gemma-4-e4b).

Usage :
    python 08_olmocr_lot.py DOSSIER_IMAGES --sortie DOSSIER_SORTIE [--modele ID] [--sans-yaml] [--tentatives 4]

Dépendance facultative : Pillow (pip install pillow), uniquement pour pivoter automatiquement une page détectée « tournée ».
"""
import argparse
import base64
import io
import json
import os
import re
import sys
import time

from lmstudio_client import post

# Prompt officiel olmOCR (olmocr/prompts/prompts.py, build_no_anchoring_v4_yaml_prompt). La coquille « LateX » est d'origine.
PROMPT_OLMOCR = (
    "Attached is one page of a document that you must process. Just return the plain text representation of this document "
    "as if you were reading it naturally. Convert equations to LateX and tables to HTML.\n"
    "If there are any figures or charts, label them with the following markdown syntax "
    "![Alt text describing the contents of the figure](page_startx_starty_width_height.png)\n"
    "Return your output as markdown, with a front matter section on top specifying values for the primary_language, "
    "is_rotation_valid, rotation_correction, is_table, and is_diagram parameters."
)
PROMPT_GENERIQUE = ("Transcris fidèlement tout le texte de ce document en Markdown (conserve les tableaux). "
                    "Ne rajoute aucun commentaire.")
TEMPERATURES = [0.1, 0.1, 0.2, 0.3, 0.5, 0.8, 0.9, 1.0]   # même progression que le pipeline officiel


def data_url(png_bytes):
    return "data:image/png;base64," + base64.b64encode(png_bytes).decode("ascii")


def separer_yaml(texte):
    """Retourne (dict_yaml, corps). Tolère l'absence d'en-tête."""
    m = re.match(r"^\s*---\s*\n(.*?)\n---\s*\n?(.*)$", texte, re.S)
    if not m:
        return {}, texte
    meta = {}
    for ligne in m.group(1).splitlines():
        if ":" in ligne:
            k, v = ligne.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2)


def pivoter(png_bytes, degres):
    try:
        from PIL import Image
    except ImportError:
        print("   (Pillow absent : rotation automatique impossible)")
        return png_bytes
    img = Image.open(io.BytesIO(png_bytes)).rotate(-degres, expand=True)   # rotation_correction : sens horaire
    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


def traiter_page(png_bytes, args):
    prompt = PROMPT_GENERIQUE if args.sans_yaml else PROMPT_OLMOCR
    erreur = None
    for essai in range(args.tentatives):
        t = TEMPERATURES[min(essai, len(TEMPERATURES) - 1)]
        corps = {
            "model": args.modele,
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": prompt},                          # texte d'abord, puis image (comme le pipeline officiel)
                {"type": "image_url", "image_url": {"url": data_url(png_bytes)}},
            ]}],
            "temperature": t,
            "max_tokens": args.max_tokens,
            "reasoning_effort": "none",
        }
        t0 = time.time()
        rep = post("/v1/chat/completions", corps)
        choix = rep["choices"][0]
        usage = rep["usage"]
        dt = time.time() - t0
        info = f"essai {essai + 1} (T={t}) : {usage['prompt_tokens']} tok entrée, {usage['completion_tokens']} tok sortie, {dt:.0f} s, fin={choix['finish_reason']}"
        if choix["finish_reason"] != "stop":
            erreur = info
            print("   ✗", info, "-> nouvel essai")
            continue
        meta, texte = (({}, choix["message"]["content"]) if args.sans_yaml else separer_yaml(choix["message"]["content"]))
        if meta.get("is_rotation_valid", "True").lower() == "false" and meta.get("rotation_correction", "0") in ("90", "180", "270"):
            print("   ↻ page tournée de", meta["rotation_correction"], "° -> rotation et nouvel essai")
            png_bytes = pivoter(png_bytes, int(meta["rotation_correction"]))
            continue
        print("   ✓", info)
        return meta, texte, usage, dt
    raise RuntimeError(f"page non traitée après {args.tentatives} essais ({erreur})")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dossier", help="dossier contenant les pages en PNG")
    ap.add_argument("--sortie", default="sortie_md", help="dossier de sortie des fichiers .md")
    ap.add_argument("--modele", default="allenai/olmocr-2-7b", help="identifiant du modèle dans LM Studio")
    ap.add_argument("--sans-yaml", action="store_true", help="prompt générique, pas d'en-tête YAML (autre modèle que OlmOCR)")
    ap.add_argument("--tentatives", type=int, default=4)
    ap.add_argument("--max-tokens", type=int, default=8000)
    args = ap.parse_args()

    pages = sorted(f for f in os.listdir(args.dossier) if f.lower().endswith(".png"))
    if not pages:
        sys.exit("Aucun fichier .png dans " + args.dossier)
    os.makedirs(args.sortie, exist_ok=True)
    total = {"entree": 0, "sortie": 0, "secondes": 0.0}
    for i, nom in enumerate(pages, 1):
        print(f"[{i}/{len(pages)}] {nom}")
        with open(os.path.join(args.dossier, nom), "rb") as f:
            meta, texte, usage, dt = traiter_page(f.read(), args)
        with open(os.path.join(args.sortie, os.path.splitext(nom)[0] + ".md"), "w", encoding="utf-8") as f:
            f.write(texte)
        if meta:
            with open(os.path.join(args.sortie, os.path.splitext(nom)[0] + ".meta.json"), "w", encoding="utf-8") as f:
                json.dump(meta, f, ensure_ascii=False, indent=1)
        total["entree"] += usage["prompt_tokens"]; total["sortie"] += usage["completion_tokens"]; total["secondes"] += dt
    print(f"\nTerminé : {len(pages)} page(s), {total['entree']} tokens en entrée, {total['sortie']} en sortie, "
          f"{total['secondes']:.0f} s ({total['sortie'] / max(total['secondes'], 1):.1f} tok/s global).")


if __name__ == "__main__":
    main()
