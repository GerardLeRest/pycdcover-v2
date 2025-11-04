#!/usr/bin/env python3
"""
Tags.py — Récupère les tags MP3 d’un CD et les enregistre dans ~/PyCDCover/tags.txt
Auteur : Gérard Le Rest (2025)
"""

from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
import os

class Titres:

    def __init__(self, L_devant, H_back_cover,titre):
        self.titre = titre
        self.L_devant = L_devant
        self.H_back_cover = H_back_cover
        # positions x et y de l'élément à placer
        self.x = 0 
        self.y = 0 
        # dossiers
        self.dossier_racine = Path(__file__).parent.parent
        dossier_utilisateur = Path.home()
        self.dossier_polices = os.path.join(self.dossier_racine, "ressources", "polices")
        self.dossier_pycovercd = dossier_utilisateur / "PyCDCover"
        os.chdir(self.dossier_pycovercd)
        
    def titre_horizontal(self):
        """Création de l'image horizontale du titre"""
        print("titre_horizontal")
        # Créer l'image blanche
        self.imageH = Image.new("RGB", (self.L_devant, 220), "white")
        self.draw = ImageDraw.Draw(self.imageH)
        os.chdir(self.dossier_polices)
        police1 = "FreeSerif.ttf"
        taille = 60
        self.font1 = ImageFont.truetype(police1, taille)
        # Calcul du centrage
        bbox = self.draw.textbbox((0, 0), self.titre, font=self.font1)
        largeur_texte = bbox[2] - bbox[0]
        self.x = (self.L_devant - largeur_texte) / 2
        self.y = 60
        # Dessiner le texte
        self.draw.text((self.x, self.y), self.titre, fill="black", font=self.font1)
        # Sauvegarder après le dessin
        chemin_image = self.dossier_pycovercd / "TitreH.png"
        self.imageH.save(chemin_image, "PNG")

    def titre_vertical1(self) -> Image.Image:
        """Création du premier titre vertical"""
        self.imageV = Image.new("RGB", (self.H_back_cover, 60), "white")
        self.draw = ImageDraw.Draw(self.imageV)
        # Récupère le dossier de ce module, même si appelé depuis l’extérieur
        # Récupère le dossier racine du projet (un niveau au-dessus de Modele)
        dossier_racine = Path(__file__).resolve().parent.parent
        police1 = f"{self.dossier_polices}/FreeSerif.ttf"
        self.font1 = ImageFont.truetype(police1, 40)
        self.draw.text((40, 5), self.titre, fill="black", font=self.font1)
        out1 = self.imageV.rotate(90, expand=True)
        chemin_image = self.dossier_pycovercd / "TitreV1.png"
        out1.save(chemin_image, "PNG")

    def titre_vertical2(self) -> Image.Image:
        """Création du deuxième titre vertical"""
        out2 = self.imageV.rotate(270, expand=True)
        chemin_image = self.dossier_pycovercd / "TitreV2.png"
        out2.save(chemin_image, "PNG")

if __name__ =="__main__":
    titre = Titres(1200, 1380, "Titre1")
    titre.titre_horizontal()
    titre.titre_vertical1()
    titre.titre_vertical2()