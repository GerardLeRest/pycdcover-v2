#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gabarit — crée le gabarit de la jaquette à découper sous forme de PDF.
"""

from reportlab.pdfgen import canvas
from PIL import Image
from PySide6.QtWidgets import QMessageBox
from pathlib import Path
import os

class Gabarit():

    def __init__(self, coefficient, L_devant, H_devant, L_back_cover, H_back_cover):
        """initialisation)"""
        self.coefficient= coefficient # coef pour pdf (résolution=72ppp; 1 pouce=254mm)
        # dimensions de l'image de devant
        self.L_devant = L_devant
        self.H_devant =  H_devant
        # dimensions de l'image de derrière
        self.L_back_cover=L_back_cover
        self.H_back_cover=H_back_cover
        #dossiers
        dossier_utilisateur = Path.home()
        # Dossier de travail de l'appli
        self.dossier_pycovercd = dossier_utilisateur / "PyCDCover"
        # Se placer dans le dossier thumbnails
        os.chdir(self.dossier_pycovercd)

    def creation_canvas(self):
        self.canv=canvas.Canvas("image_impression.pdf") # instantation d'un objet canevas reportlab
        self.canv.setLineWidth(1)
        self.canv.setDash(6,3)
     
    def creation_lignes_decoupage(self):
        """creation d'un gabarit d'impression: deux images avant et arriere + titres vericaux + trace decoupage dans une page PDF"""
        # création des lignes en 
        # pointillés de découpage
            # lignes verticales
        origines=[(300*self.coefficient,0),(360*self.coefficient,0),(1560*self.coefficient,0),(1740*self.coefficient,0),(1800*self.coefficient,0)]
        H=2970*self.coefficient
        for i in origines:
            xorigine,yorigine=i[0],i[1]
            self.canv.line(xorigine,yorigine,xorigine,yorigine+H)
        # lignes horizontales
        origines=[(0,2860*self.coefficient),(0,1660*self.coefficient),(0,480*self.coefficient)]
        L=2100*self.coefficient
        for i in origines:
            xorigine,yorigine=i[0],i[1]
            self.canv.line(xorigine,yorigine,xorigine+L,yorigine)   
           
    def insertion_images(self, L_devant, H_devant, L_back_cover, H_back_cover):

        try:
            # insertion de l'image Devant.png
            xorigine,yorigine=360*self.coefficient,1660*self.coefficient
            self.canv.drawImage("Image_thumbnails.jpeg",xorigine,yorigine, width=L_devant*self.coefficient,height=H_devant*self.coefficient,mask=None)
            # insertion de l'image Dos.png
            into=Image.open("Image_Back_Cover.png")
            L,H=into.size
            xorigine,yorigine=360*self.coefficient,480*self.coefficient
            self.canv.drawImage("Image_Back_Cover.png",xorigine,yorigine, width=L_back_cover*self.coefficient,height=H_back_cover*self.coefficient,mask=None)
            # insertion des titres verticaux
            xorigine,yorigine=300*self.coefficient,480*self.coefficient
            self.canv.drawImage("TitreV1.png",xorigine,yorigine, width=60*self.coefficient,height=H_back_cover*self.coefficient,mask=None)
            xorigine,yorigine=1740*self.coefficient,480*self.coefficient
            self.canv.drawImage("TitreV2.png",xorigine,yorigine, width=60*self.coefficient,height=H_back_cover*self.coefficient,mask=None)
            # tracé des rectangles en traits pleins
            self.canv.setDash(1,0)
            self.canv.rect(360*self.coefficient,1660*self.coefficient,L_devant*self.coefficient,H_devant*self.coefficient)
            self.canv.rect(300*self.coefficient,480*self.coefficient,60*self.coefficient,H_back_cover*self.coefficient)
            self.canv.rect(1740*self.coefficient,480*self.coefficient,60*self.coefficient,H_back_cover*self.coefficient)
            self.canv.rect(360*self.coefficient,480*self.coefficient,L_back_cover*self.coefficient,H_back_cover*self.coefficient)
            self.canv.showPage()    # sauvegarde de la page courante
            self.canv.save()    # enregistrement du fichier et fermeture du canveas reportlab
        except IOError:
            pass
            print("Toutes les images n'ont pas été créé") 


if __name__ == "__main__":
    gabarit = Gabarit(72.0/254,1200,1200,1380,1180)
    gabarit.creation_canvas()
    gabarit.creation_lignes_decoupage()
    gabarit.insertion_images(1200,1200,1380,1180)