#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Face_arriere — crée l'image de la face arrière de la jaquette
Auteur : Gérard Le Rest (2025)
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import os
from Modele.Titres import Titres


class Image_face_arriere:
    """Crée la face arrière d'une jaquette à partir du fichier tags.txt."""

    def __init__(self):
        # Dossier de travail : ~/PyCDCover/thumbnails
        self.dossier_racine = Path(__file__).parent.parent
        dossier_utilisateur = Path.home()
        self.dossier_pycdcover = dossier_utilisateur / "PyCDCover"
        self.dossier_thumbnails = self.dossier_pycdcover / "thumbnails"
        os.chdir(self.dossier_pycdcover)
        # --- Chemins vers les fichiers .ttf ---
        self.dossier_polices = os.path.join(self.dossier_racine, "ressources", "polices")
        self.police_normale = f"{self.dossier_polices}/DejaVuSans.ttf"
        self.police_grasse = f"{self.dossier_polices}/DejaVuSans-Bold.ttf"
        self.artiste = ""
        self.album = ""

    def creer_image_blanche(self)->None:
        """Lit tags.txt et génère l’image arrière."""
        fichier_tags = self.dossier_pycdcover / "tags.txt"
        # Détermination du nombre d'images dans le dossier thumbnails
        self.nb_fichiers = sum(1 for f in self.dossier_thumbnails.iterdir() if f.is_file())
        print(f"nombre de fichiers {self.nb_fichiers}")
        if not fichier_tags.exists():
            print("Fichier tags.txt introuvable.")
            return
        # Lecture du fichier (on conserve les lignes vides)
        # on enlève \n à chaque ligne
        with open(fichier_tags, "r") as f:
            self.lignes = [ligne.rstrip("\n") for ligne in f.readlines()]
        # Création de l'image blanche
        if self.nb_fichiers >= 1:  # mode multi-albums
            largeur, hauteur = 1380, 930
        else:  # maquette simple
            largeur, hauteur = 460, 460
        self.image = Image.new("RGB", (largeur, hauteur), "white")
        self.draw = ImageDraw.Draw(self.image)
        return self.draw

    def configuration(self, hauteur: float) -> None:
        """Configure les polices et les positions de départ selon la hauteur."""
        print(f"self.nb_fichiers: {self.nb_fichiers}")
        # Calculs de base 
        nbre_colonnes = 3
        nbre_lignes = len(self.lignes)
        # Taille automatique de la police (ajustée au nombre de lignes) 
        self.taille = 890 / ((nbre_lignes + 1) / nbre_colonnes)
        if self.taille > 26:
            self.taille = 26
        print(f"Taille de police calculée : {self.taille:.2f}")
        # Chargement des polices
        self.font_police = ImageFont.truetype(self.police_normale, int(self.taille))
        self.font_police_grasse = ImageFont.truetype(self.police_grasse, int(self.taille))

        # Position de départ et limites
        self.x, self.y = 20, 20
        self.ligne_max = hauteur - 5
        self.largeur_colonne = 1340 / nbre_colonnes - 10

    def cd_maquette(self, draw: ImageDraw.ImageDraw) -> None:
        """Affiche un album unique centré."""
        self.y = 100
        nbre_chansons = 0
        for i, ligne in enumerate(self.lignes):
            ligne = ligne.strip()
            if not ligne:
                continue

            if ligne.startswith("C: "):
                # Extraction du nom d’artiste
                self.artiste = ligne[3:].strip()
                continue

            elif ligne.startswith("A: "):
                # Extraction du nom d’album
                self.album = ligne[3:].strip()
                self.taille = 45

                # Police grasse avec repli sur défaut
                try:
                    self.font_police_grasse = ImageFont.truetype(self.police_grasse, int(self.taille))
                except OSError:
                    self.font_police_grasse = ImageFont.load_default()

                couleur = "darkblue"
                texte = self.album

                # Exemple d’affichage possible (à adapter selon ton contexte)
                # draw.text((self.x, self.y), texte, font=self.font_police_grasse, fill=couleur)
                
            elif i == 2:  # année et genre
                continue
            # gestion de l'espace entre le titre de l'album et la première chanson
            if nbre_chansons == 0:  # première chanson
                self.y += 40
            # Chanson suivante
            nbre_chansons += 1
            self.taille = 35
            self.font_police = ImageFont.truetype(self.police_grasse, int(self.taille))
            texte = ligne
            font = self.font_police
            couleur = "gray"
            # Cenrage sur X
            largeur_texte = draw.textlength(texte, font=font)
            x = (self.image.width - largeur_texte) // 2
            # dessin du texte
            draw.text((x, self.y), texte, fill=couleur, font=font)
            self.y += 45  # Décalage entre les lignes
            self.changer_titres_verticaux()

    def changer_titres_verticaux(self) -> None:
        "Changer les titres verticaux : artiste - album"
        texte_titre = f"{self.artiste} - {self.album}"
        titres = Titres(1200, 1380, texte_titre)
        titres.titre_vertical1()
        titres.titre_vertical2()

    def cd_multiples(self, draw) -> None:
        """Affiche plusieurs albums ; passe à la colonne suivante dès que la hauteur est dépassée."""
        lignes = self.lignes
        espace_inter_album = self.taille * 1.2  # espace vertical entre albums
        # parcours des lignes
        for ligne in lignes:
            ligne = ligne.rstrip("\n")
            # Ligne vide → espace inter-album
            if not ligne:
                self.y += espace_inter_album
                continue
            # --- Type de ligne ---
            if ligne.startswith("C: "):  # artiste
                texte = ligne[3:]
                #texte = self.couper_titre (texte, self.largeur_colonne)
                font = self.font_police_grasse
                couleur = "black"
            elif ligne.startswith("A: "):  # album
                texte = ligne[3:]
                #texte = self.couper_titre (texte, self.largeur_colonne)
                font = self.font_police_grasse
                couleur = "darkblue"
            else:  # chanson
                texte = ligne
                #texte = self.couper_titre (texte, self.largeur_colonne)
                font = self.font_police
                couleur = "gray"
            # --- Ajustement si le texte dépasse la largeur de la colonne ---
            # while draw.textbbox((0, 0), texte, font=font)[2] > (self.largeur_colonne - 10):
            #     texte = texte[:-1]
            # --- Dessin du texte ---
            draw.text((self.x, self.y), texte, fill=couleur, font=font)

            # --- Ligne suivante ---
            self.y += self.taille
            # --- Changement de colonne ---
            if self.y > self.ligne_max - self.taille:
                self.y = 20
                self.x += self.largeur_colonne + 10
    
    def sauvegarde_image(self) -> None:
        """Sauvegarde de l'image générée."""
        chemin_sortie = self.dossier_pycdcover / "Image_Back_Cover.png"
        self.image.save(chemin_sortie, "PNG")
        print(f"Image arrière enregistrée : {chemin_sortie}")


# ------------------------------------------------------------------------------
# Programme principal de test
# ------------------------------------------------------------------------------
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