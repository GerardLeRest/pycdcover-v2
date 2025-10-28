#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Face_arriere — crée l'image de la face arrière de la jaquette
Auteur : Gérard Le Rest (2025)
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os


class Image_face_arriere:
    """Crée la face arrière d'une jaquette à partir du fichier tags.txt."""

    def __init__(self):
        # Dossier de travail : ~/PyCDCover/thumbnails
        dossier_utilisateur = Path.home()
        self.dossier_pycovercd = dossier_utilisateur / "PyCDCover"
        self.dossier_thumbnails = self.dossier_pycovercd / "thumbnails"
        os.chdir(self.dossier_pycovercd)
        # Polices (polices du systeme)
        self.police_normale = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        self.police_grasse = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    def creer_image(self):
        """Lit tags.txt et génère l’image arrière."""
        chemin_tags = self.dossier_pycovercd / "tags.txt"
        if not chemin_tags.exists():
            print("Fichier tags.txt introuvable.")
            return
        # Lecture du fichier
        with open(chemin_tags, "r") as f:
            lignes = [ligne.strip() for ligne in f.readlines() if ligne.strip()]
        # Création de l'image blanche
        largeur, hauteur = 1380, 930
        image = Image.new("RGB", (largeur, hauteur), "white")
        draw = ImageDraw.Draw(image)
        # Chargement de la police
        font = ImageFont.truetype(self.police_normale, 20)
        font_bold = ImageFont.truetype(self.police_grasse, 22)
        # Position de départ
        x, y = 40, 40
        ligne_max = hauteur - 40
        # Parcours des lignes du fichier
        for ligne in lignes:
            if ligne.startswith("C: "):
                texte = ligne[3:]
                draw.text((x, y), texte, fill="black", font=font_bold)
            elif ligne.startswith("A: "):
                texte = ligne[3:]
                draw.text((x, y), texte, fill="darkblue", font=font_bold)
            else:
                draw.text((x, y), ligne, fill="gray", font=font)
            y += 28
            if y > ligne_max:
                y = 40
                x += 450  # colonne suivante
        # Sauvegarde de l'image
        chemin_sortie = self.dossier_pycovercd / "Image_Back_Cover.png"
        image.save(chemin_sortie, "PNG")
        print(f"Image arrière enregistrée : {chemin_sortie}")

if __name__ == "__main__":
    face_arriere = Image_face_arriere()
    face_arriere.creer_image()
