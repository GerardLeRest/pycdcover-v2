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


class Gabarit:
    """Créer un gabarit pour une jaquette CD à découper - format PDF"""

    def __init__(self, coefficient, L_devant, H_devant, L_back_cover, H_back_cover):
        """initialisation"""
        self.coefficient = coefficient
        self.L_devant = L_devant
        self.H_devant = H_devant
        self.L_back_cover = L_back_cover
        self.H_back_cover = H_back_cover
        # dossier utilisateur
        dossier_utilisateur = Path.home()
        # Dossier de travail de l'appli
        self.dossier_pycovercd = dossier_utilisateur / "PyCDCover"
        # Se placer dans le dossier thumbnails
        os.chdir(self.dossier_pycovercd)

    def lignes(self):
        """dessiner les lignes"""
        self.canv = canvas.Canvas("image_impression.pdf") # instantation d'un objet canevas reportlab
        self.canv.setLineWidth(1)
        self.canv.setDash(6,3)
        # création des lignes en pointillés de découpage
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

    def face(self,image_originale,largeur, hauteur):
        """création des images (face avant et dos sans titres verticaux) à imprimer"""
        im=Image.new("RGB", (largeur,hauteur), "white")
        draw = ImageDraw.Draw(im)
        into1=Image.open("TitreH.png")
        L,H=into1.size
        marge_x=(largeur-L)/2
        im.paste(into1,(0+int(marge_x),0,L+int(marge_x),H))
        im2=Image.open(image_originale)
        # redimensionnement
        L,H=im2.size
        Lf,Hf=float(L),float(H)
        rapport=Hf/Lf        # rapport hauteur/longueur de l'image
        if (L==self.L_back_cover) and (H<=930):
            out=im2 #image Image_Back_Cover.png
        elif Hf>Lf:
            L_modifie=int(960/rapport)
            out=im2.resize((L_modifie,960))
        else:
            H_modifie=int(960*rapport)
            out=im2.resize((960,H_modifie))
        L,H=out.size
        marge_x=(largeur-L)/2
        im.paste(out,(0+int(marge_x),220,L+int(marge_x),H+220))
        return im
            

    def insertion_des_images(self):
        """insertion de toutes les images"""
       # try:
        # insertion de l'image Devant.png
        xorigine, yorigine = 360*self.coefficient, 1660*self.coefficient
        self.canv.drawImage("Image_thumbnails.jpeg", xorigine, yorigine,
                            width=self.L_devant*self.coefficient,
                            height=self.H_devant*self.coefficient, mask=None)
        # insertion du titre horizontal au-dessus de la face avant
        

        # insertion de l'image Dos.png
        into = Image.open("Image_Back_Cover.png")
        L, H = into.size
        xorigine, yorigine = 360*self.coefficient, 480*self.coefficient
        self.canv.drawImage("Image_Back_Cover.png", xorigine, yorigine,
                            width=self.L_back_cover*self.coefficient,
                            height=self.H_back_cover*self.coefficient, mask=None)
        # insertion du titre horizontal au-dessus de la face arrière
        

        # insertion des titres verticaux
        xorigine, yorigine = 300*self.coefficient, 480*self.coefficient
        self.canv.drawImage("TitreV1.png", xorigine, yorigine,
                            width=60*self.coefficient,
                            height=self.H_back_cover*self.coefficient, mask=None)
        xorigine, yorigine = 1740*self.coefficient, 480*self.coefficient
        self.canv.drawImage("TitreV2.png", xorigine, yorigine,
                            width=60*self.coefficient,
                            height=self.H_back_cover*self.coefficient, mask=None)

    def trace_rectangles_trait_continu(self):
        """tracer les rectangles en trait continu"""
        # tracé des rectangles en traits pleins
        self.canv.setDash(1,0)
        self.canv.rect(360*self.coefficient,1660*self.coefficient,
                    self.L_devant*self.coefficient,self.H_devant*self.coefficient)
        self.canv.rect(300*self.coefficient,480*self.coefficient,
                    60*self.coefficient,self.H_back_cover*self.coefficient)
        self.canv.rect(1740*self.coefficient,480*self.coefficient,
                    60*self.coefficient,self.H_back_cover*self.coefficient)
        self.canv.rect(360*self.coefficient,480*self.coefficient,
                    self.L_back_cover*self.coefficient,self.H_back_cover*self.coefficient)

        # except IOError:
        #     print("Toutes les images de la jaquette n'ont pas été créées")
        
    def sauvegarde(self):
        "sauvegarde du projer reportLab"
        self.canv.showPage()    # sauvegarde de la page courante
        self.canv.save()    # enregistrement du fichier et fermeture du canveas reportlab

if __name__ == "__main__":
    gabarit = Gabarit(72.0/254,1200,1200,1380,1180)
    gabarit.lignes()
    gabarit.insertion_des_images()
    gabarit.trace_rectangles_trait_continu()
    gabarit.sauvegarde()