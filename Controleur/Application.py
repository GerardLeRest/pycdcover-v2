#!/usr/bin/env python3

"""
Application.py — Récupère les tags MP3 d’un CD et les enregistre dans ~/PyCDCover/tags.txt
Auteur : Gérard Le Rest (2025)
"""

import os, sys, shutil, platform, subprocess, webbrowser
from pathlib import Path
from PySide6.QtWidgets import QWidget, QApplication, QMessageBox, QFileDialog
from PySide6.QtCore import Slot

# Imports MVC
from Vue.Fenetre import Fenetre
from Vue.Fen_Titre import Fen_Titre
from Vue.Editeur_tags import Editeur_tags
from Vue.TelechargementUI import TelechargementUI

from Modele.Titres import Titres
from Modele.Tags import Tags
from Modele.recup_images_avant import lire_tags
from Modele.Lancement_av_ar import Lancement_av_ar
from Modele.Gabarit import Gabarit

import os, sys, shutil, platform, subprocess

class Application(QWidget):

    def __init__(self):
        """initialisation"""
        super().__init__()
        self.reinitialiser_dossier_pycdcover()
        # Toutes les méthodes et variables d’instance de Fenetre sont accessibles via :
        self.vue = Fenetre()
        self.dossier_pycdcover = Path.home() / "PyCDCover"
        # Connexions Vue → Contrôleur - BP menu
        self.vue.demande_saisie_titre.connect(self.action_titre)
        self.vue.demande_ouvrir_recuperation_tags.connect(self.action_recuperer_tags)
        self.vue.demande_ouvrir_editeur_tags.connect(self.action_ouvrir_editeur_tags)
        self.vue.demande_recuperer_images.connect(self.action_recuperer_images)
        self.vue.demande_faces.connect(self.action_faces)
        self.vue.demande_pdf.connect(self.action_pdf)
        # ------------------------------------------#
        # Connexions Vue → Contrôleur - BP "changer"
        self.vue.haut_milieu.demande_image_changee.connect(self.on_image_changee)
        self.donnees = {}
      
    def reinitialiser_dossier_pycdcover(self) -> None:
        """vider le dossier PyCDCover"""
        dossier_principal = os.path.expanduser("~/PyCDCover")
        # Supprime complètement le dossier s'il existe
        if os.path.exists(dossier_principal):
            shutil.rmtree(dossier_principal)
        # Le recrée avec le sous-dossier thumbnails
        chemin = os.path.join(dossier_principal, "thumbnails")
        if not os.path.exists(chemin):
            os.makedirs(chemin)
    
    def demarrer(self):
        """Affiche la fenêtre principale."""
        self.vue.show()
   
    @Slot()
    def action_titre(self) -> None:
        """Ouvre la fenêtre de saisie du titre."""
        self.fen_titre = Fen_Titre()
        self.fen_titre.titre_selectionne.connect(self.action_recuperer_titre)
        self.fen_titre.exec()

    @Slot(str)
    def action_recuperer_titre(self, titre_saisi: str) -> None:
        """Reçoit le titre saisi et génère les images correspondantes."""
        titres = Titres(1200, 1380, titre_saisi)
        titres.titre_horizontal()
        titres.titre_vertical1()
        titres.titre_vertical2()
        # active le bouton suivant - BP récupération de tags
        self.vue.act_recup_tags.setEnabled(True)  


    @Slot(str)
    def action_recuperer_tags(self, titre_saisi: str) -> None:
        """Reçoit le titre saisi et génère les images correspondantes."""
        # Création de l’objet métier Titres
        t = Titres(1200, 1380, titre_saisi)
        t.titre_horizontal()
        t.titre_vertical1()
        t.titre_vertical2()
        # 🔹 Activation du bouton suivant ("Récupérer les tags")
        self.vue.act_recup_tags.setEnabled(True)

    @Slot()
    def action_recuperer_tags(self) -> None:
        """Récupère les tags MP3 du CD et crée le fichier tags.txt."""
        self.tags = Tags()
        self.tags.tags_termines.connect(lambda: self.vue.act_tags_rw.setEnabled(True))
        self.tags.show()
        self.tags.recuperer_tags()
   
    
    @Slot()
    def action_ouvrir_editeur_tags(self) -> None:
        """Ouvre la fenêtre d'édition du fichier tags.txt."""
        # Instanciation 
        self.editeur_tags = Editeur_tags() 
        self.editeur_tags.show()
        # Activation du bouton suivant ("Récupérer les images")
        self.vue.act_recup_images.setEnabled(True)


    @Slot()
    def action_recuperer_images(self) -> None:
        """Récupère les images à partir du fichier tags.txt."""
        chemin_tags = Path.home() / "PyCDCover" / "tags.txt"
        if not chemin_tags.exists():
            QMessageBox.warning(None, "Fichier manquant",
                                f"Le fichier {chemin_tags} est introuvable.")
            return
        # récupérer des données des albums
        albums = lire_tags(chemin_tags)
        if not albums:
            QMessageBox.warning(None, "Aucun album trouvé",
                                "Le fichier 'tags.txt' est vide ou mal formaté.")
            return
        # Création et affichage de la fenêtre de téléchargement
        self.telechargement_ui = TelechargementUI(albums)
        self.telechargement_ui.telechargement_termine.connect(
            lambda: self.vue.act_faces.setEnabled(True)
        )
        self.telechargement_ui.show()
  
    @Slot()
    def action_faces(self) -> None:
        """Génère les deux faces (avant et arrière) de la jaquette."""
        # 🔹 Relire les données si besoin
        self.vue.recup_donnees.charger_depuis_fichier()
        self.vue.liste.clear()
        self.vue.liste.addItems(self.vue.recup_donnees.tableau)
        # 🔹 Lancer la génération (indispensable)
        lancement_av_ar = Lancement_av_ar()
        # 🔹 Activer le bouton PDF
        self.vue.act_pdf.setEnabled(True)

    @Slot()
    def action_pdf(self) -> None:
        """générer Pdf"""
        gabarit = Gabarit(0.283464567,1200,1200,1380,1180) # 72.0/254
        gabarit.lignes_pointillees()
        gabarit.insertion_images()
        gabarit.lignes_continues()
        gabarit.sauvegarde()
        # Ouvre un fichier PDF avec le lecteur par défaut du système
        systeme = platform.system()
        chemin_pdf = self.dossier_pycdcover /"image_impression.pdf"
        try:
            if systeme == "Windows":
                os.startfile(chemin_pdf)  # intégré à Windows
            elif systeme == "Darwin":  # macOS
                subprocess.run(["open", chemin_pdf])
            else:  # Linux ou autre Unix
                webbrowser.open(chemin_pdf.as_uri())
        except Exception as e:
            print(f"Erreur lors de l'ouverture du PDF : {e}")

    @Slot(str)
    def on_image_changee(self, nom_image: str) -> None:
        """Met à jour la donnée métier (nom du fichier de jaquette)."""
        # 🔹 Relance la mise à jour de la vue
        self.donnees["couverture"] = nom_image
        self.vue.haut_milieu.MAJ_haut_milieu(self.donnees)


# ------------------------------------------------------------------------------
# Programme principal de test
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    appli = Application()
    appli.vue.show()  # c’est bien self.vue dans la classe
    app.exec()
