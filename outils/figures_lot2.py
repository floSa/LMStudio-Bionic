"""Génère les figures pédagogiques du lot 2 : boucle d'appel d'outil (MCP), niveaux d'exposition du serveur, chat à état, Auto Review.
Aucune dépendance autre que pillow. Les images sont écrites dans docs/img/."""
import math
import os

from PIL import Image, ImageDraw, ImageFont

RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "img")
F = r"C:\Windows\Fonts\arial.ttf"
FB = r"C:\Windows\Fonts\arialbd.ttf"
font = lambda s, b=False: ImageFont.truetype(FB if b else F, s)
BG, INK, GREY = "#ffffff", "#1f2933", "#8896a4"
BLUE, ORANGE, GREEN, RED, PURPLE = "#2f6fdb", "#f08a24", "#2e9e6b", "#d64545", "#7a4fd1"


def sortie(sous_dossier, nom):
    p = os.path.join(RACINE, sous_dossier)
    os.makedirs(p, exist_ok=True)
    return os.path.join(p, nom)


def box(d, xy, title, sub, color, fill=None, tsize=21):
    x, y, w, h = xy
    d.rounded_rectangle((x, y, x + w, y + h), 14, outline=color, width=4, fill=fill)
    tw = d.textlength(title, font=font(tsize, True))
    d.text((x + (w - tw) / 2, y + 12), title, font=font(tsize, True), fill=color)
    d.multiline_text((x + 14, y + 48), sub, font=font(17), fill=INK, spacing=5)


def arrow(d, a, b, color=INK, width=4):
    d.line((a, b), fill=color, width=width)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for da in (2.6, -2.6):
        d.line((b, (b[0] + 16 * math.cos(ang + da), b[1] + 16 * math.sin(ang + da))), fill=color, width=width)


def figure_boucle_outil():
    img = Image.new("RGB", (1200, 560), BG)
    d = ImageDraw.Draw(img)
    d.text((40, 20), "Appel d'outil : le modèle demande, l'application exécute", font=font(30, True), fill=INK)
    box(d, (40, 100, 260, 130), "1. Question", "Message de l'utilisateur\n+ liste des outils\ndisponibles (noms, schémas).", BLUE)
    box(d, (350, 100, 260, 130), "2. Modèle", "Décide : répondre en\ntexte ou demander un\nappel d'outil (JSON).", PURPLE)
    box(d, (660, 100, 260, 130), "3. Confirmation", "Arguments affichés ;\nProceed, Deny ou\nAlways allow.", RED)
    box(d, (660, 330, 260, 130), "4. Serveur MCP", "Programme local (stdio)\nou service distant (URL)\nqui exécute l'outil.", ORANGE)
    box(d, (350, 330, 260, 130), "5. Résultat", "Texte renvoyé au modèle\net ajouté au contexte\nde la conversation.", GREEN)
    box(d, (40, 330, 260, 130), "6. Réponse", "Le modèle rédige la\nréponse finale (ou\nenchaîne un autre appel).", BLUE)
    arrow(d, (300, 165), (350, 165))
    arrow(d, (610, 165), (660, 165))
    arrow(d, (790, 230), (790, 330))
    arrow(d, (660, 395), (610, 395))
    arrow(d, (350, 395), (300, 395))
    d.line((480, 330, 480, 232), fill=GREY, width=4)
    arrow(d, (480, 262), (480, 231), GREY)
    d.text((498, 262), "nouvel appel possible", font=font(16), fill=GREY)
    d.text((40, 490), "Le modèle ne lance jamais rien lui-même : il produit du texte structuré ; l'application décide d'exécuter ou non.", font=font(17), fill=GREY)
    d.text((40, 520), "Chaque outil déclaré consomme du contexte (nom, description, schéma) à chaque requête, utilisé ou non.", font=font(17), fill=GREY)
    img.save(sortie("lmstudio/10-mcp", "00-boucle-appel-outil.png"))


def figure_exposition():
    img = Image.new("RGB", (1200, 560), BG)
    d = ImageDraw.Draw(img)
    d.text((40, 20), "Trois niveaux d'exposition du serveur local", font=font(30, True), fill=INK)
    cols = [("A. Local strict", GREEN, "Adresse 127.0.0.1",
             ["Serve on Local Network : off", "Accessible depuis ce poste seul", "Authentification : facultative", "CORS : off"], "Risque : faible"),
            ("B. Réseau local", ORANGE, "Adresse 0.0.0.0",
             ["Serve on Local Network : on", "Authentification obligatoire", "Un jeton par application", "Pare-feu : sources limitées"], "Risque : moyen"),
            ("C. Internet", RED, "Redirection de port, tunnel",
             ["Hors périmètre du produit", "Aucune protection suffisante", "Prompts et modèle exposés", "À proscrire"], "Risque : élevé")]
    for i, (t, c, adr, pts, risk) in enumerate(cols):
        x = 40 + i * 385
        d.rounded_rectangle((x, 90, x + 360, 470), 16, outline=c, width=5)
        d.text((x + 18, 106), t, font=font(26, True), fill=c)
        d.text((x + 18, 150), adr, font=font(19, True), fill=INK)
        y = 200
        for p in pts:
            d.ellipse((x + 20, y + 8, x + 30, y + 18), fill=c)
            d.text((x + 42, y), p, font=font(18), fill=INK)
            y += 44
        d.text((x + 18, 420), risk, font=font(20, True), fill=c)
    d.text((40, 495), "Le niveau réel se lit sur l'adresse d'écoute (Get-NetTCPConnection -LocalPort 1234 -State Listen), pas sur l'interface seule.", font=font(17), fill=GREY)
    img.save(sortie("lmstudio/11-securite", "00-niveaux-exposition.png"))


def figure_chat_etat():
    img = Image.new("RGB", (1200, 520), BG)
    d = ImageDraw.Draw(img)
    d.text((40, 20), "Chat à état : response_id, previous_response_id et branches", font=font(30, True), fill=INK)
    noeuds = [(60, 120, "Requête 1", "input : « Retiens ZEBRE-42 »", "response_id : r1", BLUE),
              (440, 120, "Requête 2", "previous_response_id : r1\ninput : « Quel code ? »", "response_id : r2", GREEN),
              (820, 120, "Requête 3", "previous_response_id : r2\ninput : « Ma 1re question ? »", "response_id : r3", GREEN),
              (440, 330, "Branche", "previous_response_id : r1\ninput : « En minuscules ? »", "response_id : r4", ORANGE)]
    for x, y, t, sub, rid, c in noeuds:
        d.rounded_rectangle((x, y, x + 320, y + 150), 14, outline=c, width=4)
        d.text((x + 14, y + 10), t, font=font(22, True), fill=c)
        d.multiline_text((x + 14, y + 50), sub, font=font(16), fill=INK, spacing=4)
        d.text((x + 14, y + 112), rid, font=font(17, True), fill=c)
    arrow(d, (380, 195), (440, 195))
    arrow(d, (760, 195), (820, 195))
    d.line((220, 270, 220, 405), fill=ORANGE, width=4)
    arrow(d, (220, 405), (440, 405), ORANGE)
    d.text((60, 480), "Le serveur conserve l'historique : seul le nouveau message est envoyé. « store : false » désactive ce mécanisme (pas de response_id).", font=font(17), fill=GREY)
    img.save(sortie("lmstudio/12-api-avancee", "00-chat-a-etat.png"))


def figure_auto_review():
    img = Image.new("RGB", (1200, 640), BG)
    d = ImageDraw.Draw(img)
    d.text((40, 20), "Auto Review : deux étages avant l'exécution d'une commande", font=font(30, True), fill=INK)
    box(d, (40, 100, 240, 120), "Commande", "Proposée par l'agent\n(shell ou PowerShell).", BLUE)
    box(d, (340, 100, 300, 140), "Shell Judge", "Analyseur déterministe :\nreconnaît les commandes\nde lecture sûres.", GREEN)
    box(d, (730, 100, 300, 140), "Exécution", "Approuvée sans modèle.\nSortie renvoyée à l'agent.", GREEN)
    box(d, (340, 330, 300, 150), "Shell Reviewer", "Sous-agent (modèle) :\nnote le risque, l'accord\nde l'utilisateur et la\ncorrection de la commande.", ORANGE)
    arrow(d, (280, 160), (340, 160))
    arrow(d, (640, 170), (730, 170), GREEN)
    d.text((655, 128), "reconnue", font=font(16), fill=GREEN)
    arrow(d, (490, 240), (490, 330), ORANGE)
    d.text((505, 268), "non reconnue", font=font(16), fill=ORANGE)
    sorties = [(730, 300, "low", "Exécutée si l'utilisateur\nn'a rien refusé.", GREEN),
               (730, 400, "high", "Exécutée seulement si\nl'utilisateur l'a demandée\n(sinon : confirmation).", ORANGE),
               (730, 510, "too_destructive", "Jamais exécutée,\nmême sur demande.", RED)]
    for x, y, t, sub, c in sorties:
        d.rounded_rectangle((x, y, x + 300, y + 92), 12, outline=c, width=4)
        d.text((x + 12, y + 6), t, font=font(20, True), fill=c)
        d.multiline_text((x + 12, y + 36), sub, font=font(15), fill=INK, spacing=3)
        arrow(d, (640, 405), (x, y + 46), c, 3)
    d.text((40, 590), "Principe issu du blog officiel ; l'ordre de grandeur « jusqu'à 82 % des commandes approuvées sans modèle » est une valeur annoncée par l'éditeur [Source].", font=font(15), fill=GREY)
    img.save(sortie("bionic/12-auto-review", "00-pipeline-auto-review.png"))


def figure_integrations():
    img = Image.new("RGB", (1200, 560), BG)
    d = ImageDraw.Draw(img)
    d.text((40, 20), "Outils tiers et routes du serveur local (127.0.0.1:1234)", font=font(30, True), fill=INK)
    clients = [("Claude Code", PURPLE, "/v1/messages"), ("Codex (--oss)", BLUE, "/v1/responses"),
               ("Cline, Roo Code", GREEN, "/v1/chat/completions"), ("Continue", ORANGE, "/v1/chat/completions\n/v1/completions, /v1/embeddings"),
               ("Open WebUI", GREEN, "/v1/models, /v1/chat/completions"), ("Aider", ORANGE, "/v1/chat/completions")]
    for i, (nom, c, route) in enumerate(clients):
        y = 90 + i * 70
        d.rounded_rectangle((40, y, 300, y + 56), 12, outline=c, width=4)
        d.text((56, y + 14), nom, font=font(21, True), fill=c)
        d.multiline_text((330, y + 2), route, font=font(16), fill=INK, spacing=2)
        arrow(d, (300, y + 46), (780, min(max(y + 46, 130), 450)), c, 2)
    d.rounded_rectangle((780, 90, 1160, 480), 16, outline=INK, width=5)
    d.text((800, 106), "Serveur LM Studio", font=font(26, True), fill=INK)
    for k, t in enumerate(["Authentification (jeton)", "Chargement à la volée (JIT)", "Modèle chargé", "Journaux (prompts en clair)"]):
        d.rounded_rectangle((800, 160 + k * 70, 1140, 210 + k * 70), 10, outline=GREY, width=3)
        d.text((816, 174 + k * 70), t, font=font(19), fill=INK)
    d.text((40, 520), "Une clé quelconque suffit sans authentification ; avec authentification, chaque outil doit recevoir un jeton réel.", font=font(17), fill=GREY)
    img.save(sortie("lmstudio/13-integrations", "00-outils-et-routes.png"))


if __name__ == "__main__":
    figure_boucle_outil()
    figure_exposition()
    figure_chat_etat()
    figure_auto_review()
    figure_integrations()
    print("figures générées")
