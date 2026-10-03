"""Génère les figures pédagogiques du Manuel 00 (notions fondamentales) à partir de valeurs mesurées ou calculées."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "img", "lmstudio", "00-notions")
os.makedirs(OUT, exist_ok=True)
F = r"C:\Windows\Fonts\arial.ttf"
FB = r"C:\Windows\Fonts\arialbd.ttf"
font = lambda s, b=False: ImageFont.truetype(FB if b else F, s)
BG, INK, GRID = "#ffffff", "#1f2933", "#d9dee3"
BLUE, ORANGE, GREEN, RED, PURPLE, GREY = "#2f6fdb", "#f08a24", "#2e9e6b", "#d64545", "#7a4fd1", "#8896a4"


def centered(d, xy, text, f, fill=INK):
    w = d.textlength(text, font=f)
    d.text((xy[0] - w / 2, xy[1]), text, font=f, fill=fill)


def figure_decodage():
    img = Image.new("RGB", (1200, 560), BG); d = ImageDraw.Draw(img)
    d.text((40, 24), "Lire le nom d'une quantification : exemple Q4_K_M", font=font(30, True), fill=INK)
    parts = [("Q", BLUE, "Quantifié", "Les nombres du modèle\nsont compressés."),
             ("4", ORANGE, "≈ 4 bits par poids", "Plus ce nombre est bas,\nplus le fichier est petit\n(et moins précis)."),
             ("K", GREEN, "Méthode « K-quants »", "Compression par blocs\navec échelles : meilleure\nqualité à taille égale."),
             ("M", PURPLE, "Medium (moyen)", "Dosage : S (small),\nM (medium), L (large).\nPlus gros = plus de couches\nsensibles gardées en\nhaute précision.")]
    xs = [230, 470, 700, 930]
    big = font(120, True)
    # Q 4 _ K _ M
    layout = [("Q", 230, BLUE), ("4", 395, ORANGE), ("_", 470, GREY), ("K", 585, GREEN), ("_", 650, GREY), ("M", 790, PURPLE)]
    for t, x, c in layout:
        d.text((x, 90), t, font=big, fill=c)
    anchors = [(265, BLUE, parts[0]), (430, ORANGE, parts[1]), (625, GREEN, parts[2]), (830, PURPLE, parts[3])]
    y0 = 250
    for x, c, (_, _, title, desc) in anchors:
        d.line((x, 225, x, y0), fill=c, width=4)
        d.ellipse((x - 7, y0 - 7, x + 7, y0 + 7), fill=c)
    boxes = [(40, 270, BLUE), (320, 270, ORANGE), (610, 270, GREEN), (900, 270, PURPLE)]
    for (bx, by, c), (_, _, (_, _, title, desc)) in zip(boxes, anchors):
        d.rounded_rectangle((bx, by, bx + 265, by + 230), 14, outline=c, width=4)
        d.text((bx + 14, by + 12), title, font=font(21, True), fill=c)
        d.text((bx + 14, by + 52), desc, font=font(18), fill=INK, spacing=5)
    for (bx, by, c), (ax, _, _) in zip(boxes, anchors):
        d.line((ax, y0, bx + 132, by), fill=c, width=3)
    d.text((40, 520), "Autres noms fréquents : Q8_0 (≈ 8 bits, quasi sans perte) · Q6_K · Q5_K_M · IQ (très compressé) · F16 / BF16 (non compressé)", font=font(17), fill=GREY)
    img.save(os.path.join(OUT, "01-decodage-q4-k-m.png"))


def figure_tailles():
    data = [("F16 / BF16", 15.24, 16.0, GREY), ("Q8_0", 8.10, 8.5, BLUE), ("Q6_K", 6.25, 6.56, BLUE), ("Q5_K_M", 5.44, 5.7, GREEN),
            ("Q4_K_M", 4.68, 4.9, GREEN), ("Q3_K_M", 3.81, 4.0, ORANGE), ("Q2_K", 3.02, 3.2, RED)]
    img = Image.new("RGB", (1200, 560), BG); d = ImageDraw.Draw(img)
    d.text((40, 20), "Taille d'un même modèle (≈ 7,6 milliards de paramètres) selon sa quantification", font=font(26, True), fill=INK)
    left, top, scale = 220, 90, 46   # px par Go
    for i, (nom, go, bpw, c) in enumerate(data):
        y = top + i * 56
        d.text((40, y + 8), nom, font=font(22, True), fill=INK)
        d.rounded_rectangle((left, y, left + go * scale, y + 40), 6, fill=c)
        d.text((left + go * scale + 12, y + 7), f"{go:.2f} Go  ·  ≈ {bpw} bits/poids  ·  {go / 15.24 * 100:.0f} %", font=font(19), fill=INK)
    d.line((left, top - 8, left, top + 7 * 56), fill=GRID, width=2)
    d.text((40, 490), "Qualité : ◄ plus fidèle à l'original                                                      plus compressé, plus de pertes ►", font=font(18), fill=GREY)
    d.text((40, 520), "Source des tailles : fichiers GGUF publiés d'OlmOCR 2 7B (partie texte, hors adaptateur de vision).", font=font(15), fill=GREY)
    img.save(os.path.join(OUT, "02-taille-selon-quantification.png"))


def figure_memoire():
    ctx = [("2 048", 6.31), ("8 192", 6.61), ("32 768", 7.83), ("65 536", 9.45), ("131 072", 12.69)]
    img = Image.new("RGB", (1200, 560), BG); d = ImageDraw.Draw(img)
    d.text((40, 20), "Mémoire d'un modèle chargé selon la taille de contexte (exemple mesuré : Gemma 4 E4B, Q4_K_M)", font=font(24, True), fill=INK)
    base = 6.31
    left, top, scale = 200, 90, 60
    for i, (nom, tot) in enumerate(ctx):
        y = top + i * 70
        d.text((40, y + 10), nom + " tokens", font=font(20, True), fill=INK)
        d.rectangle((left, y, left + base * scale, y + 44), fill=BLUE)
        extra = tot - base
        if extra > 0.005:
            d.rectangle((left + base * scale, y, left + tot * scale, y + 44), fill=ORANGE)
        d.text((left + tot * scale + 12, y + 10), f"{tot:.2f} Go", font=font(20), fill=INK)
    ly = 470
    d.rectangle((left, ly, left + 24, ly + 24), fill=BLUE); d.text((left + 34, ly), "Modèle (poids) + tampons de calcul : ≈ 6,3 Go, constant", font=font(19), fill=INK)
    d.rectangle((left, ly + 34, left + 24, ly + 58), fill=ORANGE); d.text((left + 34, ly + 34), "Cache KV : croît avec le contexte (≈ 50 Ko par token)", font=font(19), fill=INK)
    img.save(os.path.join(OUT, "03-memoire-selon-contexte.png"))


def figure_pile():
    img = Image.new("RGB", (1200, 640), BG); d = ImageDraw.Draw(img)
    d.text((40, 18), "De l'application au matériel : où s'insèrent les « runtimes »", font=font(28, True), fill=INK)

    def box(x, y, w, h, title, sub, c, fill=None):
        d.rounded_rectangle((x, y, x + w, y + h), 14, fill=fill or "#f4f7fb", outline=c, width=4)
        centered(d, (x + w / 2, y + 12), title, font(21, True), c)
        centered(d, (x + w / 2, y + 44), sub, font(16), INK)

    box(300, 80, 600, 80, "LM Studio (interface, serveur, API)", "ce que l'utilisateur voit et appelle", BLUE)
    box(300, 190, 600, 80, "Moteur d'inférence : llama.cpp (format GGUF)", "lit le modèle et calcule les réponses", GREEN)
    for x, t, s, c in [(40, "Runtime CPU", "calcul sur le processeur", GREY), (330, "Runtime CUDA", "cartes graphiques Nvidia", GREEN),
                       (620, "Runtime Vulkan", "GPU Intel, AMD, Nvidia", ORANGE), (910, "Metal / MLX", "Mac Apple Silicon", PURPLE)]:
        box(x, 330, 250, 80, t, s, c)
        d.line((x + 125, 300, x + 125, 330), fill=c, width=3)
    d.line((165, 300, 1035, 300), fill=GREEN, width=3)
    d.line((600, 270, 600, 300), fill=GREEN, width=3)
    for x, t, s, c in [(40, "Processeur (CPU)", "+ mémoire RAM", GREY), (330, "GPU Nvidia", "+ mémoire VRAM", GREEN),
                       (620, "GPU intégré ou dédié", "VRAM ou RAM partagée", ORANGE), (910, "Puce Apple", "mémoire unifiée", PURPLE)]:
        box(x, 470, 250, 80, t, s, c, fill="#fffaf2")
        d.line((x + 125, 410, x + 125, 470), fill=c, width=3)
    d.rounded_rectangle((40, 575, 1160, 625), 10, outline=RED, width=3)
    d.text((56, 585), "Harmony : n'est PAS un moteur de calcul. Format de conversation d'OpenAI : décode les messages et les « canaux » de raisonnement.", font=font(17), fill=INK)
    img.save(os.path.join(OUT, "04-pile-moteur-materiel.png"))


def figure_bande_passante():
    img = Image.new("RGB", (1200, 420), BG); d = ImageDraw.Draw(img)
    d.text((40, 18), "Deux phases, deux limites", font=font(28, True), fill=INK)
    d.rounded_rectangle((40, 80, 580, 380), 14, outline=BLUE, width=4)
    d.text((60, 92), "1. Lecture du prompt (« prompt processing »)", font=font(22, True), fill=BLUE)
    d.text((60, 135), "Le modèle lit toute la question d'un coup.\n\nLimite : la puissance de CALCUL.\n\nPlus de calcul (GPU) = plus rapide.\nMesuré : 215 → 353 tok/s\n(CPU seul → GPU intégré).", font=font(19), fill=INK, spacing=4)
    d.rounded_rectangle((620, 80, 1160, 380), 14, outline=ORANGE, width=4)
    d.text((640, 92), "2. Écriture de la réponse (« génération »)", font=font(22, True), fill=ORANGE)
    d.text((640, 135), "Un mot (token) à la fois ; à chaque mot,\nle modèle est relu en mémoire.\n\nLimite : la BANDE PASSANTE mémoire.\n\nvitesse ≈ bande passante ÷ taille lue\nMesuré : 11,2 → 14,8 tok/s.", font=font(19), fill=INK, spacing=4)
    img.save(os.path.join(OUT, "05-deux-phases-calcul-memoire.png"))


if __name__ == "__main__":
    figure_decodage(); figure_tailles(); figure_memoire(); figure_pile(); figure_bande_passante()
    print("figures écrites dans", os.path.abspath(OUT))
