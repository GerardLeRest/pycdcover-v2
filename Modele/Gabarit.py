#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gabarit — crée le gabarit de la jaquette à découper sous forme de PDF.
Version avec titres horizontaux visibles, en haut des faces avant et arrière.
"""

from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw
from pathlib import Path
import os
import glob


class Gabarit:
    """Créer un gabarit pour une jaquette CD à découper - format PDF"""

    def __init__(self, coefficient, L_devant, H_devant, L_back_cover, H_back_cover):
        """initialisation"""
        self.L_devant = L_devant
        self.H_devant = H_devant
        self.L_back_cover = L_back_cover
        self.H_back_cover = H_back_cover
        self.coefficient = coefficient
        # dossier utilisateur
        dossier_utilisateur = Path.home()
        # Dossier de travail de l'appli
        self.dossier_pycovercd = dossier_utilisateur / "PyCDCover"
        # Se placer dans le dossier thumbnails
        os.chdir(self.dossier_pycovercd)

    def compter_images_thumbnails(self):
        """Compte les images présentes dans ~/PyCDCover/thumbnails/."""
        dossier = os.path.expanduser("~/PyCDCover/thumbnails")
        motifs = ("*.jpg", "*.jpeg", "*.png")
        fichiers = []
        for motif in motifs:
            fichiers.extend(glob.glob(os.path.join(dossier, motif)))
        return len(fichiers)

    def lignes_pointillees(self):
        """dessiner les lignes"""
        self.canv = canvas.Canvas("image_impression.pdf") # instantation d'un objet canevas reportlab
        self.canv.setLineWidth(1)
        self.canv.setDash(6,3)
        # création des lignes en pointillés de découpage
            # lignes verticales
        origines=[(300*self.coefficient,0),(360*self.coefficient,0),(1740*self.coefficient,0),(1800*self.coefficient,0)]
        H=2950*self.coefficient
        for i in origines:
            xorigine,yorigine=i[0],i[1]
            self.canv.line(xorigine,yorigine,xorigine,yorigine+H)
        # lignes horizontales
        origines=[(0,2860*self.coefficient),(0,1660*self.coefficient),(0,480*self.coefficient)]
        L=2100*self.coefficient
        for i in origines:
            xorigine,yorigine=i[0],i[1]
            self.canv.line(xorigine,yorigine,xorigine+L,yorigine)      

    def face(self, image_originale, largeur, hauteur):
        """création des images (face avant et dos sans titres verticaux) à imprimer"""
        im = Image.new("RGB", (largeur, hauteur), "white")  # création de l'image blanche
        compteur = self.compter_images_thumbnails()
        if compteur > 1:
            # insertion du titre horizontal
            into1 = Image.open("TitreH.png")
            L, H = into1.size
            marge_x = (largeur - L) / 2
            # descendre le titre davantage si un seul CD
            decalage_titre = 60 if os.path.exists("tags.txt") and len(open("tags.txt").readlines()) < 20 else 40
            im.paste(into1, (int(marge_x), decalage_titre, int(marge_x) + L, decalage_titre + H))
            # ouverture et traitement de l'image principale000
            im2 = Image.open(image_originale)
            # redimensionnement
            L, H = im2.size
            Lf, Hf = float(L), float(H)
            rapport = Hf / Lf  # rapport hauteur/longueur de l'image
            if (L == largeur) and (H <= hauteur):
                out = im2  # image Image_Back_Cover.png
            elif Hf > Lf:
                L_modifie = int(960 / rapport)
                out = im2.resize((L_modifie, 960))
            else:
                H_modifie = int(960 * rapport)
                out = im2.resize((960, H_modifie))
            # collage de l'image dans le gabarit
            L, H = out.size
            marge_x = (largeur - L) / 2
            im.paste(out, (int(marge_x), 220, int(marge_x) + L, H + 220))
        else: # maquette
            im2 = Image.open(image_originale)
            out = im2.resize((1200, 1200)) # l'image à placer est aussi grande que l'image blanche
            im.paste(out, (0, 40)) # en haut à gauche
        return im 

    
    def insertion_images(self):
        """création et insertion de toutes les images"""
        #try:
            # création de la face avant
        image_titre = self.face("Image_thumbnails.jpeg", self.L_devant, self.H_devant) 
        image_titre.save("Devant.jpeg", "jpeg")
        # création de la face arrière
        image_dos = self.face("Image_Back_Cover.png", self.L_back_cover, self.H_back_cover)
        image_dos.save("Dos.png", "png")
        os.chdir(self.dossier_pycovercd)  # sécurité pour le chemin de travail
        # insertion de l'image Devant
        xorigine, yorigine = 360 * self.coefficient, 1700 * self.coefficient
        self.canv.drawImage("Devant.jpeg", xorigine, yorigine,
                            width=self.L_devant * self.coefficient,
                            height=self.H_devant * self.coefficient, mask=None)
        # insertion de l'image Dos
        xorigine, yorigine = 400 * self.coefficient, 520 * self.coefficient
        self.canv.drawImage("Dos.png", xorigine, yorigine,
                            width=self.L_back_cover * self.coefficient,
                            height=self.H_back_cover * self.coefficient, mask=None)
        # insertion des titres verticaux
        xorigine, yorigine = 300 * self.coefficient, 480 * self.coefficient
        self.canv.drawImage("TitreV1.png", xorigine, yorigine,
                            width=60 * self.coefficient,
                            height=self.H_back_cover * self.coefficient, mask=None)
        xorigine, yorigine = 1740 * self.coefficient, 480 * self.coefficient
        self.canv.drawImage("TitreV2.png", xorigine, yorigine,
                            width=60 * self.coefficient,
                            height=self.H_back_cover * self.coefficient, mask=None)
        # except IOError:
        #     print("Toutes les images de la jaquette n'ont pas été créées")

    def lignes_continues (self):        
        """tracé des rectangles"""
        self.canv.setDash(1, 0)
        self.canv.rect(360 * self.coefficient, 1660 * self.coefficient,
                    self.L_devant * self.coefficient, self.H_devant * self.coefficient)
        self.canv.rect(300 * self.coefficient, 480 * self.coefficient,
                    60 * self.coefficient, self.H_back_cover * self.coefficient)
        self.canv.rect(1740 * self.coefficient, 480 * self.coefficient,
                    60 * self.coefficient, self.H_back_cover * self.coefficient)
        self.canv.rect(360 * self.coefficient, 480 * self.coefficient,
                    self.L_back_cover * self.coefficient, self.H_back_cover * self.coefficient)
            
    
    def sauvegarde(self):
        """sauvegarde"""
        self.canv.showPage()
        self.canv.save()


if __name__ == "__main__":
    gabarit = Gabarit(0.283464567,1200,1200,1380,1180) # 72.0/254
    nombre_images = gabarit.compter_images_thumbnails()
    gabarit.lignes_pointillees()
    gabarit.insertion_images()
    gabarit.lignes_continues()
    gabarit.sauvegarde()