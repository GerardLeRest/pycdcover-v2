#!/usr/bin/env python3

"""
Titre.py - Crée les images des titres (horizontal et verticaux) pour la jaquette CD
Auteur : Gérard Le Rest (2025)
"""

from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
import os


class Titres:
    """Crée les images des titres (horizontal et verticaux) pour la jaquette CD."""

    def __init__(self, L_devant: int, H_back_cover: int, titre: str) -> None:
        self.titre = titre
        self.L_devant = L_devant
        self.H_back_cover = H_back_cover
        self.x = 0
        self.y = 0
        # dossiers
        self.dossier_racine = Path(__file__).parent.parent
        self.dossier_polices = self.dossier_racine / "ressources" / "polices"
        self.dossier_pycdcover = Path.home() / "PyCDCover"

    def titre_horizontal(self) -> None:
        """Création de l'image horizontale du titre"""
        imageH = Image.new("RGB", (self.L_devant, 220), "white")
        draw = ImageDraw.Draw(imageH)
        police1 = self.dossier_polices / "FreeSerif.ttf"
        try:
            font1 = ImageFont.truetype(str(police1), 60)
        except OSError:
            font1 = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), self.titre, font=font1)
        largeur_texte = bbox[2] - bbox[0]
        x = (self.L_devant - largeur_texte) / 2
        y = 60
        draw.text((x, y), self.titre, fill="black", font=font1)
        imageH.save(self.dossier_pycdcover / "TitreH.png", "PNG")

    def titre_vertical1(self) -> None:
        """Création du premier titre vertical"""
        imageV = Image.new("RGB", (self.H_back_cover, 60), "white")
        draw = ImageDraw.Draw(imageV)
        police1 = self.dossier_polices / "FreeSerif.ttf"
        try:
            font1 = ImageFont.truetype(str(police1), 40)
        except OSError:
            font1 = ImageFont.load_default()
        draw.text((40, 5), self.titre, fill="black", font=font1)
        out1 = imageV.rotate(90, expand=True)
        out1.save(self.dossier_pycdcover / "TitreV1.png", "PNG")
        self.imageV = imageV  # pour la réutilisation par titre_vertical2

    def titre_vertical2(self) -> None:
        """Création du deuxième titre vertical"""
        if hasattr(self, "imageV"):
            out2 = self.imageV.rotate(270, expand=True)
            out2.save(self.dossier_pycdcover / "TitreV2.png", "PNG")

# -----------------------------------------------------------
# --- Test manuel -------------------------------------------
# -----------------------------------------------------------

if __name__ == "__main__":
    titre = Titres(1200, 1380, "Titre1")
    titre.titre_horizontal()
    titre.titre_vertical1()
    titre.titre_vertical2()
