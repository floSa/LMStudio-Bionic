"""Vérifie la cohérence de la documentation : images et liens relatifs existants, ancres internes, ton (pronoms personnels, pictogrammes)."""
import os, re, sys, unicodedata

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DOCS = os.path.join(ROOT, "docs")
md_files = []
for base, _, files in os.walk(DOCS):
    md_files += [os.path.join(base, f) for f in files if f.endswith(".md")]
md_files.append(os.path.join(ROOT, "README.md"))
md_files.append(os.path.join(ROOT, "outils", "README.md"))


def slug(title):
    t = title.strip().lower()
    t = re.sub(r"[`*]", "", t)
    t = re.sub(r"[^\w\s\-àâäéèêëîïôöùûüçœæ]", "", t, flags=re.UNICODE)
    return re.sub(r"\s", "-", t)


def anchors(path):
    out = set()
    in_code = False
    for line in open(path, encoding="utf-8"):
        if line.startswith("```"):
            in_code = not in_code
        if not in_code and re.match(r"^#{1,6} ", line):
            out.add(slug(re.sub(r"^#{1,6} ", "", line)))
    return out


problems = []
anchor_cache = {}
for f in md_files:
    text = open(f, encoding="utf-8").read()
    rel = os.path.relpath(f, ROOT)
    for m in re.finditer(r"!?\[[^\]]*\]\(([^)\s]+)\)", re.sub(r"`[^`\n]*`", "", re.sub(r"```.*?```", "", text, flags=re.S))):
        target = m.group(1)
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        path, _, frag = target.partition("#")
        full = os.path.normpath(os.path.join(os.path.dirname(f), path)) if path else f
        if not os.path.exists(full):
            problems.append(f"{rel}: cible absente -> {target}")
            continue
        if frag and full.endswith(".md"):
            anchor_cache.setdefault(full, anchors(full))
            if frag not in anchor_cache[full]:
                problems.append(f"{rel}: ancre introuvable -> {target}")
    # ton
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    body = re.sub(r"`[^`]*`", "", body)
    for pat in (r"\bvous\b", r"\bnous\b", r"\bnotre\b", r"\bnos\b", r"\bvotre\b", r"\bvos\b"):
        for m in re.finditer(pat, body, flags=re.I):
            ctx = body[max(0, m.start() - 50): m.end() + 40].replace("\n", " ")
            problems.append(f"{rel}: ton -> « {ctx} »")
    if re.search(r"[\U0001F300-\U0001FAFF✅⚠❓\U0001F4DA\U0001F9EE]", body):
        problems.append(f"{rel}: pictogramme présent")

print(f"{len(md_files)} fichiers Markdown vérifiés ; {len(problems)} point(s) à traiter")
for p in problems:
    print(" -", p)
sys.exit(1 if problems else 0)
