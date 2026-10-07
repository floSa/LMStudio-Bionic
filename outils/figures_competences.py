"""Génère la figure du manuel Bionic 13 : les deux façons de déclencher une compétence (automatique, manuelle avec @)."""
import os

from figures_lot2 import ORANGE, BLUE, GREEN, GREY, INK, PURPLE, BG, arrow, box, font, sortie
from PIL import Image, ImageDraw


def figure_competences():
    img = Image.new("RGB", (1200, 600), BG)
    d = ImageDraw.Draw(img)
    d.text((40, 20), "Une compétence, deux façons de la déclencher", font=font(30, True), fill=INK)
    box(d, (40, 90, 520, 110), "Compétence globale", "~/.lmstudio/skills/<nom>/SKILL.md\nDisponible dans tous les projets.", BLUE)
    box(d, (640, 90, 520, 110), "Compétence de projet", "<dossier du projet>/.agents/skills/<nom>/SKILL.md\nToujours active dans ce projet.", GREEN)
    d.text((40, 235), "A. Déclenchement automatique", font=font(22, True), fill=PURPLE)
    etapes_a = [("Description", "nom + description\ndans le prompt système"), ("Décision", "l'agent juge la\ncompétence pertinente"),
                ("Lecture", "l'agent lit SKILL.md\n(outil de fichiers)"), ("Application", "les consignes guident\nla réponse")]
    for i, (t, sub) in enumerate(etapes_a):
        x = 40 + i * 290
        box(d, (x, 270, 250, 110), t, sub, PURPLE, tsize=20)
        if i < 3:
            arrow(d, (x + 250, 325), (x + 290, 325), PURPLE)
    d.text((40, 405), "B. Déclenchement manuel (@)", font=font(22, True), fill=ORANGE)
    etapes_b = [("Saisie", "taper @ puis le nom\ndans la zone de saisie"), ("Palette", "choisir la compétence\n(filtrage à la frappe)"),
                ("Injection", "le contenu de SKILL.md\nest joint au message"), ("Application", "les consignes guident\nla réponse")]
    for i, (t, sub) in enumerate(etapes_b):
        x = 40 + i * 290
        box(d, (x, 440, 250, 110), t, sub, ORANGE, tsize=20)
        if i < 3:
            arrow(d, (x + 250, 495), (x + 290, 495), ORANGE)
    d.text((40, 565), "Champs de SKILL.md : name, description (obligatoires) ; display-name, disable-model-invocation, user-invocable (facultatifs).",
           font=font(16), fill=GREY)
    img.save(sortie("bionic/13-competences", "00-declenchements.png"))


if __name__ == "__main__":
    figure_competences()
    print("figure générée")
