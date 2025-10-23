#!/usr/bin/env python3
"""
Lancer la création des deux images de la jaquette
Auteur : Gérard Le Rest (2025)
"""

from Modele.Image_face_avant import Image_face_avant
from Modele.Image_face_arriere import Image_face_arriere

class Lancement_av_ar:

    def __init__(self):
        # lancement de la création de l'image de la face avant
        image_face_avant = Image_face_avant()
        image_face_avant.preparation_assemblage_photos()
        image_face_avant.assemblage_photos()
        # lancement de la création de l'image de la face aarrière
        face_arriere = Image_face_arriere()
        face_arriere.creer_image()

# ------------------------------------------------------------------------------
# Programme principal de test
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    lancement_av_ar = Lancement_av_ar()
