#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Face_avant — crée la mosaïque d'images à partir d’un répertoire choisi,
et enregistre le résultat sous ~/PyCDCover/Image_thumbnails.jpeg
"""

import os
from tkinter import *
import tkinter.filedialog, tkinter.messagebox
from math import ceil, sqrt
from PIL import Image
from pathlib import Path

formats_3 = ('bmp','gif','jpg','msp','pcx','png','ppm','xbm')
formats_4 = ('jpeg','tiff')


class Face_avant:
    def __init__(self, largeur=300, hauteur=300, env_home=None, repertoire=None):
        self.largeur = largeur
        self.hauteur = hauteur
        # Répertoires de travail
        repertoire_utilisateur = Path.home()
        self.repertoire_pycovercd = repertoire_utilisateur / "PyCDCover"
        self.repertoire_thumbnails = self.repertoire_pycovercd / "thumbnails"
        # Se placer dans le répertoire PyCDCover
        os.chdir(self.repertoire_pycovercd)
        self.fichiers = []
        self.photos = []

    def preparation_images(self):
        """Choix du répertoire des images et création des miniatures"""
        self.repertoire_images = tkinter.filedialog.askdirectory(
            initialdir=self.env_home,
            title="Choisir le répertoire des images"
        )
        if not self.repertoire_images:
            return

        fichiers = os.listdir(self.repertoire_images)
        N = 1
        for fichier in fichiers:
            ext = fichier.lower().split('.')[-1]
            if ext in formats_3 or ext in formats_4:
                chemin_image = os.path.join(self.repertoire_images, fichier)
                try:
                    im = Image.open(chemin_image)
                    out = im.resize((self.largeur, self.hauteur))
                    nom_image = f"im{N}.jpeg"
                    out.save(os.path.join(self.repertoire_thumbnails, nom_image), "jpeg")
                    N += 1
                except Exception as e:
                    print(f"Erreur sur {fichier} : {e}")

    def preparation_assemblage_photos(self):
        """Prépare les dimensions de la mosaïque finale"""
        self.fichiers = os.listdir(self.repertoire_thumbnails)
        total = len(self.fichiers)
        self.NiL = ceil(sqrt(total))
        self.NiH = ceil(total / self.NiL)
        self.NiD = total % self.NiL
        self.Larg_Im_fin = self.NiL * self.largeur + (self.NiL + 1) * 10
        self.Haut_Im_fin = self.NiH * self.hauteur + (self.NiH + 1) * 10

    def assemblage_photos(self):
        """Assemble toutes les miniatures en une seule image"""
        try:
            im = Image.new("RGB", (self.Larg_Im_fin, self.Haut_Im_fin), "white")
            index = 0
            for j in range(self.NiH):
                for i in range(self.NiL):
                    if index >= len(self.fichiers):
                        break

                    chemin_image = os.path.join(self.repertoire_thumbnails, self.fichiers[index])
                    into = Image.open(chemin_image)

                    if j == self.NiH - 1 and self.NiD != 0:
                        marge = int((self.Larg_Im_fin - self.NiD * (self.largeur + 10) + 10) / 2)
                        x = marge + (self.largeur + 10) * i
                    else:
                        x = 10 + (self.largeur + 10) * i

                    y = 10 + (self.hauteur + 10) * j
                    im.paste(into, (x, y, x + self.largeur, y + self.hauteur))
                    index += 1

            sortie = os.path.join(self.repertoire_pycovercd, "Image_thumbnails.jpeg")
            im.save(sortie, "jpeg")

        except ZeroDivisionError:
            tkinter.messagebox.showinfo("Info", "Aucune image trouvée")


#########################################################################
if __name__ == "__main__":
    face_avant = Face_avant(300, 300, "/home/gerard", "/home/gerard/PyCDCover")
    face_avant.preparation_images()
    face_avant.preparation_assemblage_photos()
    face_avant.assemblage_photos()
    image_finale = os.path.join(face_avant.repertoire_pycovercd, "Image_thumbnails.jpeg")
    print("Image finale créée :", image_finale)
