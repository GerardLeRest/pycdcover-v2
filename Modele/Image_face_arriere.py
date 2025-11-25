#!/usr/bin/env python3

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
        '''initialisation'''
        # Dossiers principaux
        self.dossier_racine: Path = Path(__file__).parent.parent
        dossier_utilisateur: Path = Path.home()
        self.dossier_pycdcover: Path = dossier_utilisateur / "PyCDCover"
        self.dossier_thumbnails: Path = self.dossier_pycdcover / "thumbnails"
        self.fichier_tags: Path = self.dossier_pycdcover / "tags.txt"
        # Polices
        self.dossier_polices: str = os.path.join(self.dossier_racine, "ressources", "polices")
        self.police_normale: str = f"{self.dossier_polices}/DejaVuSans.ttf"
        self.police_grasse: str = f"{self.dossier_polices}/DejaVuSans-Bold.ttf"
        # Métadonnées du CD
        self.artiste: str | None = None
        self.album: str | None = None
        self.lignes: list[str] = []
        self.nb_fichiers: int = 0
        # Dessin
        self.image: Image.Image | None = None
        self.draw: ImageDraw.ImageDraw | None = None
        self.taille: int = 0
        self.x: int = 0
        self.y: int = 0
            

    def creer_image_blanche(self):
        """Lit tags.txt, choisit la taille, crée l'image blanche et renvoie draw."""
        # Lire les lignes du fichier
        with open(self.fichier_tags, "r") as f:
            self.lignes = [ligne.rstrip("\n") for ligne in f.readlines()]
        # Nombre d'images dans thumbnails
        self.nb_fichiers = sum(1 for f in self.dossier_thumbnails.iterdir() if f.is_file())
        # Deux tailles différentes
        if self.nb_fichiers > 1:
            largeur, hauteur = 1380, 930
        else:
            largeur, hauteur = 460, 460
        # Image blanche
        self.image = Image.new("RGB", (largeur, hauteur), "white")
        self.draw = ImageDraw.Draw(self.image)
        return self.draw

    
    def configuration(self, hauteur: float) -> None:
        """Configure les polices et les positions de départ selon la hauteur."""
        # Calculs de base 
        nbre_colonnes = 3
        nbre_lignes = len(self.lignes)
        # Taille automatique de la police (ajustée au nombre de lignes) 
        self.taille = 890 / ((nbre_lignes + 1) / nbre_colonnes)
        if self.taille > 26:
            self.taille = 26
        # Chargement des polices
        self.font_police = ImageFont.truetype(self.police_normale, int(self.taille))
        self.font_police_grasse = ImageFont.truetype(self.police_grasse, int(self.taille))
        # Position de départ et limites
        self.x, self.y = 20, 20
        self.ligne_max = hauteur - 5
        self.largeur_colonne = 1340 / nbre_colonnes - 10

    def cd_maquette(self, draw: ImageDraw.ImageDraw) -> None:
        """Affiche un album unique centré avec ajustement automatique entre les lignes."""
        self.y = 30
        # On compte le nombre de chansons
        chansons = []
        for i, ligne in enumerate(self.lignes):
            ligne = ligne.strip()
            if not ligne:
                continue
            if i >= 2:
                chansons.append(ligne)
        nbre_chansons = len(chansons)
        # Ajustement automatique de l'espacement
        # (Evite que les titres débordent dans la zone du bas)
        if nbre_chansons <= 8:
            espace = 36
        elif nbre_chansons <= 12:
            espace = 30
        else:
            espace = 20
        # Deuxième parcours pour affichage
        for i, ligne in enumerate(self.lignes):
            ligne = ligne.strip()
            if not ligne:
                continue
            # Chanteur(s)
            if ligne.startswith("C: "):
                self.artiste = ligne[3:].strip()
                continue
            # Album
            elif ligne.startswith("A: "):
                self.album = ligne[3:].strip()
                self.taille = 20
                self.dessiner( self.taille, self.album, "blue", self.font_police_grasse )
                self.y += 36
                continue
            # Chansons
            elif i > 2: # on évite le genre et l'annnée
                self.taille = 16
                self.dessiner(self.taille, ligne, "gray", self.font_police)
                self.y += espace
        self.changer_titres_verticaux()

    def dessiner(self, taille: int, texte: str, couleur: str, font: ImageFont.FreeTypeFont) -> None:
        """Dessine une ligne avec une taille ajustée sans modifier les polices originales."""
        # Crée une police temporaire avec la même famille et la taille demandée
        police_temp = ImageFont.truetype(font.path, taille)
        # Centrage horizontal
        largeur_texte = self.draw.textlength(texte, font=police_temp)
        x = (self.image.width - largeur_texte) // 2
        # Dessin
        self.draw.text((x, self.y), texte, fill=couleur, font=police_temp)

    def changer_titres_verticaux(self) -> None:
        "Changer les titres verticaux : artiste - album"
        texte_titre = f"{self.artiste} - {self.album}"
        titres = Titres(1200, 1380, texte_titre)
        titres.titre_vertical1()
        titres.titre_vertical2()

    def cd_multiples(self, draw) -> None:
        """Affiche plusieurs albums ; passe à la colonne suivante dès que la hauteur est dépassée."""
        espace_inter_album = self.taille * 1.2  # espace vertical entre albums
        # parcours des lignes
        for ligne in self.lignes:
            ligne = ligne.rstrip("\n")
            # Ligne vide → espace inter-album
            if not ligne:
                self.y += espace_inter_album
                continue
            # Type de ligne 
            if ligne.startswith("C:"):   # artiste
                texte = ligne[3:]
                font = self.font_police_grasse
                couleur = "black"
            elif ligne.startswith("A:"):  # album
                texte = ligne[3:]
                font = self.font_police_grasse
                couleur = "darkblue"
            else:  # chanson
                texte = ligne
                font = self.font_police
                couleur = "gray"
            draw.text((self.x, self.y), texte, fill=couleur, font=font)
            # Ligne suivante
            self.y += self.taille
            # Changement de colonne
            if self.y > self.ligne_max - self.taille:
                self.y = 20
                self.x += self.largeur_colonne + 10

        
    def sauvegarde_image(self) -> None:
        """Sauvegarde de l'image générée."""
        chemin_sortie = self.dossier_pycdcover / "Image_Back_Cover.png"
        self.image.save(chemin_sortie, "PNG")

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