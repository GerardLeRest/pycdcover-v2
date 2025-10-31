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
        self.dossier_racine = self.dossier_racine = Path(__file__).parent.parent
        dossier_utilisateur = Path.home()
        self.dossier_pycovercd = dossier_utilisateur / "PyCDCover"
        self.dossier_thumbnails = self.dossier_pycovercd / "thumbnails"
        os.chdir(self.dossier_pycovercd)
        # Polices (polices du systeme)
        self.dossier_polices = os.path.join(self.dossier_racine, "ressources", "polices")
        self.police_normale = f"{self.dossier_polices}/DejaVuSans.ttf"
        self.police_grasse = f"{self.dossier_polices}/DejaVuSans-Bold.ttf"
        self.hauteur, self.largeur = 0,0 # dimension de l'image
        self.lignes = [] # liste des lignes du ficher tags.txt

    def creer_image_blanche(self):
        """Lit tags.txt et génère l’image arrière."""
        fichier_tags = self.dossier_pycovercd / "tags.txt"   
        #détermination du nombre d'images
        self.nb_fichiers = sum(1 for f in self.dossier_thumbnails.iterdir() if f.is_file())
        print(f"nombre de fichiers {self.nb_fichiers}")
        if not fichier_tags.exists():
            print("Fichier tags.txt introuvable.")
            return
        # Lecture du fichier
        with open(fichier_tags, "r") as f:
            self.lignes = [ligne.strip() for ligne in f.readlines() if ligne.strip()]
        # Création de l'image blanche
        if self.nb_fichiers >= 1:    # maquette CD
            largeur, hauteur = 1380, 930
        else:
            largeur, hauteur = 460, 460
        self.image = Image.new("RGB", (largeur, hauteur), "white")
        self.draw = ImageDraw.Draw(self.image)
        return self.draw

    def configuration(self, hauteur):
        # Chargement de la police
        if self.nb_fichiers > 1:
            self.font = ImageFont.truetype(self.police_normale, 20)
            self.font_bold = ImageFont.truetype(self.police_grasse, 22)
        else:
            # Mode album unique : plus grand texte
            self.font = ImageFont.truetype(self.police_normale, 30)
            self.font_bold = ImageFont.truetype(self.police_grasse, 35)
        # Position de départ
        if self.nb_fichiers > 1:
            self.x, self.y = 40, 40
            self.ligne_max = hauteur - 40
            self.espace = 28
        else:
            # cd maquette
            self.x = 0  # on ne fixe plus x ici (calculé dynamiquement)
            self.y = 30
            self.espace = 60

    def cd_maquette(self, draw):
        """Affiche un album unique centré."""
        for i, ligne in enumerate(self.lignes):
            if ligne.startswith("C: "):
                continue
            elif ligne.startswith("A: "):
                texte = ligne[3:]
                font = self.font_bold
                couleur = "darkblue"
                self.y += 20    
            elif i==2:  # année et genre
                continue
            else:
                texte = ligne
                font = self.font
                couleur = "gray"

            largeur_texte = draw.textlength(texte, font=font)
            x = (self.image.width - largeur_texte) // 2
            draw.text((x, self.y), texte, fill=couleur, font=font)
            self.y += self.espace
    
    def cd_multiples(self, draw):
        """écrire les lignes sur un CD multiple"""
        for ligne in self.lignes:
            if ligne.startswith("C: "):
                texte = ligne[3:]
                draw.text((self.x,self.y), texte, fill="black", font=self.font_bold)
            elif ligne.startswith("A: "):
                texte = ligne[3:]
                draw.text((self.x, self.y), texte, fill="darkblue", font=self.font_bold)
            else:
                self.draw.text((self.x, self.y), ligne, fill="gray", font=self.font)
            self.y += 28
            if self.y > self.ligne_max:
                self.y = self.espace
                self.x += 450  # colonne suivante
    
    def sauvegarde_image(self)->None:
        # Sauvegarde de l'image
        chemin_sortie = self.dossier_pycovercd / "Image_Back_Cover.png"
        self.image.save(chemin_sortie, "PNG")
        print(f"Image arrière enregistrée : {chemin_sortie}")

if __name__ == "__main__":
    face_arriere = Image_face_arriere()
    draw1 = face_arriere.creer_image_blanche()
    face_arriere.configuration(930)
    if draw1 is None:
        exit("Erreur : impossible de créer l’image (vérifie tags.txt et thumbnails/)")
    # Sélection du mode
    if face_arriere.nb_fichiers > 1:
        face_arriere.cd_multiples(draw1)
    else:
        face_arriere.cd_maquette(draw1)
    # Sauvegarde
    face_arriere.sauvegarde_image()