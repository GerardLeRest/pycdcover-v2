#!/usr/bin/env python3
"""
Face_avant — créer l'image de la face avant de la jaquette
Auteur : Gérard Le Rest (2025)
"""

import os
import tkinter.messagebox
from math import ceil, sqrt
from pathlib import Path
from PIL import Image
import glob

formats_3 = ('bmp','gif','jpg','msp','pcx','png','ppm','xbm')
formats_4 = ('jpeg','tiff')


class Image_face_avant:
    """créer l'image avant de la jaquette"""
    
    def __init__(self, largeur=300, hauteur=300, env_home=None, repertoire=None):
        self.largeur = largeur
        self.hauteur = hauteur
        #dossiers
        dossier_utilisateur = Path.home()
        # Dossier de travail de l'appli
        self.dossier_pycdcover = dossier_utilisateur / "PyCDCover"
        # Sous-dossier thumbnails (déjà créé par Application)
        self.thumbnail_path = self.dossier_pycdcover / "thumbnails"
        # Se placer dans le dossier thumbnails
        os.chdir(self.dossier_pycdcover)
        # initialisation des variables
        self.dossier = ""
        self.fichiers = []
        self.photos = []
  
    
    def preparation_assemblage_photos(self) -> None:
        """Prépare les dimensions de la grille en fonction du nombre d’images."""
        self.fichiers = os.listdir(self.thumbnail_path) # nombre d'images
        total = len(self.fichiers)
        self.NiL = ceil(sqrt(total))           # nombre d’images en largeur
        self.NiH = ceil(total / self.NiL)      # nombre d’images en hauteur
        self.NiD = total % self.NiL            # nombre d’images sur la dernière ligne
        self.Larg_Im_fin = self.NiL * self.largeur + (self.NiL + 1) * 10
        self.Haut_Im_fin = self.NiH * self.hauteur + (self.NiH + 1) * 10

    def assemblage_photos(self) -> None:
        """Assemble les miniatures du dossier thumbnails pour créer la jaquette."""
        try:
            im = Image.new("RGB", (self.Larg_Im_fin, self.Haut_Im_fin), "white")
            index = 0
            for j in range(self.NiH):
                for i in range(self.NiL):
                    if index >= len(self.fichiers):
                        break

                    # ouverture de l’image à coller
                    chemin_image = self.thumbnail_path / self.fichiers[index]
                    into = Image.open(chemin_image)

                    # si dernière ligne incomplète, centrer horizontalement
                    if j == self.NiH - 1 and self.NiD != 0:
                        marge = int((self.Larg_Im_fin - self.NiD * (self.largeur + 10) + 10) / 2)
                        x = marge + (self.largeur + 10) * i
                    else:
                        x = 10 + (self.largeur + 10) * i

                    y = 10 + (self.hauteur + 10) * j

                    # assure l’égalité entre la largeur et la hauteur
                    if into.size != (self.largeur, self.hauteur):
                        into = into.resize((self.largeur, self.hauteur), Image.LANCZOS)
                    if into.mode != "RGB":
                        into = into.convert("RGB")

                    im.paste(into, (x, y, x + self.largeur, y + self.hauteur))
                    index += 1

            # sauvegarde de la mosaïque finale
            sortie = self.dossier_pycdcover / "Image_thumbnails.jpeg"
            im.save(sortie, "jpeg")

        except ZeroDivisionError:
            tkinter.messagebox.showinfo("Info", "Aucune image trouvée")
    

# ------------------------------------------------------------------------------
# Programme principal de test
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    face = Image_face_avant()
    face.preparation_assemblage_photos()
    face.assemblage_photos()

