#!/usr/bin/env python3

"""
Face_avant — créer l'image de la face avant de la jaquette
Auteur : Gérard Le Rest (2025)
"""
import os
from math import ceil, sqrt
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import glob

formats_3 = ('bmp','gif','jpg','msp','pcx','png','ppm','xbm')
formats_4 = ('jpeg','tiff')


class Image_face_avant:
    """créer l'image avant de la jaquette"""
    
    def __init__(
        self,
        largeur: int = 300,
        hauteur: int = 300,
        env_home: str | None = None,
        repertoire: str | None = None
    ):
        # Dimensions de l'image finale
        self.largeur: int = largeur
        self.hauteur: int = hauteur
        # Données et résultats
        self.nb_fichiers: int = 0
        self.lignes: list[str] = []
        self.image: Image.Image | None = None
        self.draw: ImageDraw.ImageDraw | None = None
        self.taille: int = 0
        self.x: int = 0
        self.y: int = 0
        self.ligne_max: int = 0
        self.largeur_colonne: int = 0
        # Polices
        self.font_police: ImageFont.FreeTypeFont | None = None
        self.font_police_grasse: ImageFont.FreeTypeFont | None = None
        # Fond
        self.fond: Image.Image | None = None
        # Paramètres de mosaïque
        self.NiL: int = 0        # nombre d'images en largeur
        self.Nid: int = 0        # nombre d'images en hauteur
        self.Larg_Im_fin: int = 0
        self.Haut_Im_fin: int = 0

        # Liste des fichiers importés
        self.fichiers: list[Path] = []
        self.photos: list[Image.Image] = []

        # Fichiers détectés dans thumbnails
        self.total: int = 0

        # Dossiers de travail
        dossier_utilisateur: Path = Path.home()
        self.dossier_pycdcover: Path = dossier_utilisateur / "PyCDCover"
        self.thumbnail_path: Path = self.dossier_pycdcover / "thumbnails"

        # Se placer dans ~/PyCDCover
        os.chdir(self.dossier_pycdcover)

        # Dossier courant (optionnel)
        self.dossier: str = repertoire if repertoire else ""

    
    def preparation_assemblage_photos(self) -> None:
        """Prépare les dimensions de la grille en fonction du nombre d’images."""
        self.fichiers = os.listdir(self.thumbnail_path) # nombre d'images
        total = len(self.fichiers)
        self.NiL = ceil(sqrt(total))           # nombre d’images en largeur
        self.NiH = ceil(total / self.NiL)      # nombre d’images en hauteur
        self.NiD = total % self.NiL            # nombre d’images sur la dernière ligne
        self.Larg_Im_fin = self.NiL * self.largeur + (self.NiL + 1) * 10
        self.Haut_Im_fin = self.NiH * self.hauteur + (self.NiH + 1) * 10

    def rendre_carre(self, img):
        """rendre l'image carré sans transformation"""
        w, h = img.size
        s = min(w, h)
        x = (w - s) // 2
        y = (h - s) // 2
        return img.crop((x, y, x + s, y + s))

    def assemblage_photos(self) -> None:
        """Assemble les miniatures du dossier thumbnails pour l'image."""
        try:
            # recharge la liste des fichiers
            self.fichiers = os.listdir(self.thumbnail_path)
            self.total = len(self.fichiers)

            # création d'une image blanche finale (ex : 320x320)
            self.fond = Image.new("RGB", (self.Larg_Im_fin, self.Haut_Im_fin), "white")
        
            # un ou plusieurs fichiers ?
            if self.total == 1:
                self.assemblage_une_image()
            else:
                self.assemblage_plusieurs_images()

            # sauvegarde finale
            sortie = self.dossier_pycdcover / "Image_thumbnails.jpeg"
            self.fond.save(sortie, "jpeg")

        except ZeroDivisionError:
            print("Info: Aucune image trouvée")
    
    def assemblage_une_image(self) -> None:
        """Cas - 1 seule mag - maquette"""
        # charge l'unique miniature
        chemin_image = self.thumbnail_path / self.fichiers[0]
        img = Image.open(chemin_image)
        # redimensionne SANS déformer
        img.thumbnail((self.Larg_Im_fin, self.Haut_Im_fin), Image.LANCZOS)
        # centre l'image dans le carré
        x = (self.Larg_Im_fin - img.width) // 2
        y = (self.Haut_Im_fin - img.height) // 2 + 10
        # colle sur l'image finale
        self.fond.paste(img, (x, y))

    def assemblage_plusieurs_images(self) -> None:
        """Mosaïque carrée quand il y a plusieurs miniatures."""
        
        index = 0

        for j in range(self.NiH):
            for i in range(self.NiL):
                if index >= self.total:
                    break
                # chemin de l’image à insérer
                chemin_image = self.thumbnail_path / self.fichiers[index]
                into = Image.open(chemin_image)
                # recadrage carré
                into = self.rendre_carre(into)
                # redimensionnement exact
                into = into.resize((self.largeur, self.hauteur), Image.LANCZOS)
                # centrage dernière ligne incomplète
                if j == self.NiH - 1 and self.NiD != 0:
                    marge = int((self.Larg_Im_fin - self.NiD * (self.largeur + 10) + 10) / 2)
                    x = marge + (self.largeur + 10) * i
                else:
                    x = 10 + (self.largeur + 10) * i
                # position verticale
                y = 10 + (self.hauteur + 10) * j
                # collage sur le fond final
                self.fond.paste(into, (x, y, x + self.largeur, y + self.hauteur))
                index += 1


    

# ------------------------------------------------------------------------------
# Programme principal de test
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    face = Image_face_avant()
    face.preparation_assemblage_photos()
    face.assemblage_photos()

