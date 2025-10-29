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

# ------------------------------------------------------------------------------
# Programme principal de test
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    lancement_av_ar = Lancement_av_ar()

