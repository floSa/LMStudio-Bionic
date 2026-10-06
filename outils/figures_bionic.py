"""Génère les figures pédagogiques du manuel Bionic 00 (notions de l'agent)."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "img", "bionic", "00-notions")
os.makedirs(OUT, exist_ok=True)
F = r"C:\Windows\Fonts\arial.ttf"
FB = r"C:\Windows\Fonts\arialbd.ttf"
font = lambda s, b=False: ImageFont.truetype(FB if b else F, s)
BG, INK, GRID = "#ffffff", "#1f2933", "#d9dee3"
BLUE, ORANGE, GREEN, RED, PURPLE, GREY = "#2f6fdb", "#f08a24", "#2e9e6b", "#d64545", "#7a4fd1", "#8896a4"


def box(d, xy, title, sub, color, fill=None):
    x, y, w, h = xy
    d.rounded_rectangle((x, y, x + w, y + h), 14, outline=color, width=4, fill=fill)
    tw = d.textlength(title, font=font(21, True))
    d.text((x + (w - tw) / 2, y + 12), title, font=font(21, True), fill=color)
    d.multiline_text((x + 14, y + 48), sub, font=font(17), fill=INK, spacing=5)


def arrow(d, a, b, color=INK, width=4):
    d.line((a, b), fill=color, width=width)
    import math
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for da in (2.6, -2.6):
        d.line((b, (b[0] + 16 * math.cos(ang + da), b[1] + 16 * math.sin(ang + da))), fill=color, width=width)


def figure_boucle():
    img = Image.new("RGB", (1200, 600), BG); d = ImageDraw.Draw(img)
    d.text((40, 20), "La boucle de l'agent : un modèle qui agit par étapes", font=font(30, True), fill=INK)
    box(d, (40, 100, 250, 120), "1. Consigne", "Tâche formulée en\nlangage naturel.", BLUE)
    box(d, (350, 100, 250, 120), "2. Modèle", "Décide : répondre ou\nappeler un outil.", PURPLE)
    box(d, (660, 100, 250, 120), "3. Appel d'outil", "Lire / écrire un fichier,\nlancer une commande,\nchercher sur le web.", ORANGE)
    box(d, (660, 320, 250, 150), "4. Autorisation", "Selon le mode : accord\nautomatique, vérification\npar un modèle ou\nconfirmation manuelle.", RED)
    box(d, (350, 320, 250, 150), "5. Exécution", "L'outil agit sur le dossier\nde travail ou le bac à\nsable. Le résultat est\nrenvoyé au modèle.", GREEN)
    box(d, (40, 320, 250, 150), "6. Réponse finale", "Quand la tâche est\nterminée : résumé,\nfichiers et diffs.", BLUE)
    arrow(d, (290, 160), (350, 160)); arrow(d, (600, 160), (660, 160))
    arrow(d, (785, 220), (785, 320)); arrow(d, (660, 385), (600, 385))
    arrow(d, (350, 385), (290, 385))
    # retour vers le modèle
    d.line((475, 320, 475, 220), fill=GREY, width=4); arrow(d, (475, 250), (475, 221), GREY)
    d.text((492, 262), "retour au modèle :\ntant que la tâche n'est pas\nterminée, nouvelle étape", font=font(16), fill=GREY, spacing=4)
    d.text((40, 510), "Chaque tour de boucle ajoute du texte au contexte (commande, sortie, contenu de fichier) : une tâche longue consomme beaucoup de contexte.", font=font(17), fill=GREY)
    d.text((40, 540), "Un chat classique correspond aux étapes 1, 2 et 6 uniquement : aucune action sur la machine.", font=font(17), fill=GREY)
    img.save(os.path.join(OUT, "01-boucle-agent.png"))


def figure_lieux():
    img = Image.new("RGB", (1200, 560), BG); d = ImageDraw.Draw(img)
    d.text((40, 20), "Où s'exécute le modèle : trois possibilités", font=font(30, True), fill=INK)
    cols = [("Local", GREEN, "Le modèle tourne sur\nl'ordinateur.",
             ["Rien ne quitte la machine", "Pas de compte ni de crédits", "Limité par la RAM / VRAM", "Taille et qualité du modèle\nbornées par le matériel"]),
            ("Remote (LM Link)", BLUE, "Le modèle tourne sur un\nautre appareil lié.",
             ["Calcul sur l'autre appareil", "La conversation reste sur\nl'appareil qui utilise Bionic", "Connexion au compte demandée\npar l'application (appairage)", "Disponible tant que l'appareil\nlié est allumé"]),
            ("Cloud", ORANGE, "Le modèle tourne dans le\nLM Studio Secure Cloud.",
             ["Les données quittent la machine\n(traitement transitoire, ZDR)", "Compte + crédits requis", "Pas de mémoire locale utilisée", "Modèles de grande taille"])]
    for i, (t, c, sub, pts) in enumerate(cols):
        x = 40 + i * 385
        d.rounded_rectangle((x, 90, x + 360, 500), 16, outline=c, width=5)
        d.text((x + 18, 106), t, font=font(26, True), fill=c)
        d.multiline_text((x + 18, 150), sub, font=font(18), fill=INK, spacing=5)
        y = 220
        for p in pts:
            d.ellipse((x + 20, y + 8, x + 30, y + 18), fill=c)
            d.multiline_text((x + 42, y), p, font=font(18), fill=INK, spacing=4)
            y += 58 if "\n" in p else 44
    d.text((40, 515), "Zero Data Retention (ZDR) : engagement du service cloud de ne pas conserver les données traitées [Source : documentation officielle].", font=font(15), fill=GREY)
    img.save(os.path.join(OUT, "02-lieux-execution.png"))


def figure_modes():
    img = Image.new("RGB", (1200, 520), BG); d = ImageDraw.Draw(img)
    d.text((40, 20), "Les quatre modes d'autorisation du shell (du plus prudent au plus permissif)", font=font(28, True), fill=INK)
    modes = [("Désactivé", GREEN, "Aucune commande\nn'est exécutée.", "Risque : nul"),
             ("Demander à\nchaque fois", BLUE, "Chaque commande est\nsoumise à confirmation.", "Risque : faible\n(charge de relecture)"),
             ("Vérification\nautomatique", ORANGE, "Un modèle examine la\ncommande avant exécution\n(mode par défaut).", "Risque : moyen\n(dépend du vérificateur)"),
             ("Tout autoriser", RED, "Toute commande est\nexécutée sans question.", "Risque : élevé")]
    for i, (t, c, sub, risk) in enumerate(modes):
        x = 40 + i * 285
        h = 150 + i * 30
        y = 470 - h - 40
        d.rounded_rectangle((x, y, x + 260, 470 - 40 + 40), 14, outline=c, width=5, fill="#fafbfc")
        d.multiline_text((x + 16, y + 12), t, font=font(23, True), fill=c, spacing=3)
        d.multiline_text((x + 16, y + 74), sub, font=font(17), fill=INK, spacing=4)
        d.multiline_text((x + 16, 470 - 56), risk, font=font(17, True), fill=c, spacing=3)
    d.text((40, 490), "Les modifications de fichiers dans le dossier de travail ne passent pas par ce mécanisme (constat sur le poste de test).", font=font(15), fill=GREY)
    img.save(os.path.join(OUT, "03-modes-autorisation-shell.png"))


if __name__ == "__main__":
    figure_boucle(); figure_lieux(); figure_modes()
    print("figures ok")
