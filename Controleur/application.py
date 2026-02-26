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
from Vue.fenetre import Fenetre
from Vue.fen_titre import FenTitre
from Vue.editeur_tags import Editeur_tags
from Vue.progression_images import Progress_images
from Vue.progression_tags import Progression_tags
from Vue.fen_couleur import FenCouleur
from Modele.titres import Titres
from Modele.tags import Tags
from Modele.recup_images_avant import lire_tags
from Modele.construire_faces import Lancement_av_ar
from Modele.gabarit import Gabarit
from Vue.haut_gauche import HautGauche

import os, sys, shutil, platform, subprocess

class Application(QWidget):

    def __init__(self):
        """initialisation"""
        super().__init__()
        self.reinitialiser_dossier_pycdcover()
        # Toutes les méthodes et variables d’instance de Fenetre sont accessibles via :
        self.haut_gauche = HautGauche()
        self.vue = Fenetre()
        self.dossier_pycdcover = Path.home() / "PyCDCover"
        # Connexions Vue → Contrôleur - BP menu
        self.vue.demande_saisie_titre.connect(self.action_titre)
        self.vue.demande_ouvrir_recuperation_tags.connect(self.action_recuperer_tags)
        self.vue.demande_ouvrir_editeur_tags.connect(self.action_ouvrir_editeur_tags)
        self.vue.demande_recuperer_images.connect(self.action_recuperer_images)
        self.vue.demande_couleur_dos.connect(self.action_couleur_dos)
        self.vue.demande_faces.connect(self.action_faces)
        self.vue.demande_pdf.connect(self.action_pdf)
        # ------------------------------------------#
        # Connexions Vue → Contrôleur - BP "changer"
        self.vue.haut_milieu.demande_image_changee.connect(self.changer_image)
        self.donnees = {}
        self.titre="" # titre du CD
        self.couleur ="#ffffff" # couleur de fond des deux faces des pochettes
      
    def reinitialiser_dossier_pycdcover(self) -> None:
        """vider le dossier PyCDCover"""
        dossier_principal = os.path.expanduser("~/PyCDCover")
        # Supprime complètement le dossier s'il existe
        if os.path.exists(dossier_principal):
            shutil.rmtree(dossier_principal)
        # Le recrée avec le sous-dossier "miniatures"
        chemin = os.path.join(dossier_principal, "miniatures")
        if not os.path.exists(chemin):
            os.makedirs(chemin)
    
    def demarrer(self):
        """Affiche la fenêtre principale."""
        self.vue.show()
   
    @Slot()
    def action_titre(self) -> None:
        """Ouvre la fenêtre de saisie du titre."""
        self.fen_titre = FenTitre()
        self.fen_titre.titre_selectionne.connect(self.action_recuperer_titre)
        self.fen_titre.exec()

    @Slot(str)
    def action_recuperer_titre(self, titre_saisi: str) -> None:
        """Reçoit le titre saisi et génère les images correspondantes."""
        self.titre_saisi = titre_saisi # mémorisation du titre
        titres = Titres(1200, 1380, "#F5F5F0", titre_saisi)
        titres.titre_horizontal()
        titres.titre_vertical1()
        titres.titre_vertical2()
        # active le bouton suivant - BP récupération de tags
        self.vue.act_recup_tags.setEnabled(True)

    @Slot()
    def action_recuperer_tags(self) -> None:
        """Récupérer les tags"""
        # 1. Choix du dossier (sans progression)
        progression_tmp = Progression_tags()
        chemin = progression_tmp.choisir_dossier_chansons()
        if not chemin:
            return
        chemin = Path(chemin)
        # 2. Calcul réel du nombre de MP3
        total = len(list(chemin.rglob("*.mp3")))
        # 3. Aucun MP3 → message et stop
        if total == 0:
            progression_tmp.absence_mp3(0)
            return
        # 4. Maintenant seulement, on crée la fenêtre de progression
        self.progress_tags = Progression_tags()
        self.progress_tags.defilement(total)
        self.progress_tags.show()
        # 5. Modèle
        self.tags = Tags()
        # 6. Connexions
        self.tags.progress.connect(
            self.progress_tags.progress.setValue
        )
        self.tags.termine.connect(
            self.progress_tags.fermeture_fenetre_progress
        )
        self.progress_tags.tags_termines.connect(
            lambda: self.vue.act_tags_rw.setEnabled(True)
        )
        # 7. Lancement du traitement
        self.tags.extraire_tags(chemin)
   
    @Slot()
    def action_ouvrir_editeur_tags(self) -> None:
        """Ouvre la fenêtre d'édition du fichier tags.txt."""
        # Fenêtre d’édition SANS parent pour éviter les histoires d’empilement
        self.editeur_tags = Editeur_tags()  
        # Quand on ferme/valide, on recharge les albums
        self.editeur_tags.tags_enregistres.connect(self.haut_gauche.charger_depuis_fichier)
        self.editeur_tags.show()
        # Bouton suivant activé
        self.vue.act_recup_images.setEnabled(True)

    @Slot()
    def action_couleur_dos(self)->None: 
        """sélectionner la couleur du dos de la pochette"""
        self.fen_couleur = FenCouleur()
        self.fen_couleur.couleur_selectionnee.connect(self.action_recuperer_couleur)
        self.fen_couleur.exec()
        self.vue.act_faces.setEnabled(True)

    @Slot(str)
    def action_recuperer_couleur(self, couleur: str) -> None:
        """ajouter la couleur aux fonds des titres"""
        self.couleur = couleur # mémorisation de la couleur pour la suite
        titres = Titres(1200, 1380, self.couleur, self.titre_saisi)  # ✅ titre ajouté
        titres.titre_horizontal()
        titres.titre_vertical1()
        titres.titre_vertical2()
        self.vue.act_recup_tags.setEnabled(True)

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
        self.telechargement_ui = Progress_images(albums)
        self.telechargement_ui.telechargement_termine.connect(
            lambda:self.vue.act_couleur_dos.setEnabled(True)
        )
        self.telechargement_ui.show()
  
    @Slot()
    def action_faces(self) -> None:
        """Génère les deux faces (avant et arrière) de la jaquette."""
        # self.recup_donnees = Haut_Gauche() - voir fenetre.py
        self.vue.haut_gauche.charger_depuis_fichier() 
        self.vue.liste.clear()
        # clé: artiste-album de self.tableau
        self.vue.liste.addItems(self.vue.haut_gauche.liste_artistes_albums)
        # Lancer la génération
        lancement_av_ar = Lancement_av_ar(self.couleur)
        # Activer le bouton PDF
        self.vue.act_pdf.setEnabled(True)

    @Slot()
    def action_pdf(self) -> None:
        """générer Pdf"""
        gabarit = Gabarit(0.283464567,1200,1200,1380,1180, self.couleur) # 72.0/254
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
    def changer_image(self, nom_image: str) -> None:
        """Met à jour la donnée métier (nom du fichier de jaquette)."""
        # 🔹 Relance la mise à jour de la vue
        self.donnees["couverture"] = nom_image
        self.vue.haut_milieu.MAJ_haut_milieu(self.donnees)

    def mettre_a_jour_liste_albums(self) -> None:
        """Recharge les données albums après modification des tags."""
        self.haut_gauche.charger_depuis_fichier()


# ------------------------------------------------------------------------------
# Programme principal de test
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    appli = Application()
    appli.vue.show()  # c’est bien self.vue dans la classe
    app.exec()