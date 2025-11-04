#!/usr/bin/env python3
"""
Application.py — Récupère les tags MP3 d’un CD et les enregistre dans ~/PyCDCover/tags.txt
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Slot
import sys, os
from Vue.Fenetre import Fenetre
from Vue.Fen_Titre import Fen_Titre
from Modele.Titres import Titres
import shutil  
from pathlib import Path
from Modele.Tags import Tags

class Application(QWidget):

    def __init__(self):
        """initialisation"""
        super().__init__()
        self.reinitialiser_dossier_pycdcover()
        self.fenetre = Fenetre()
        self.fenetre.demande_saisie_titre.connect(self.activer_titre)

    def reinitialiser_dossier_pycdcover(self)->None:
        """vider le dossier PyCDCover"""
        dossier_principal = os.path.expanduser("~/PyCDCover")
        # Supprime complètement le dossier s'il existe
        if os.path.exists(dossier_principal):
            shutil.rmtree(dossier_principal)
        # Le recrée avec le sous-dossier thumbnails
        chemin = os.path.join(dossier_principal, "thumbnails")
        if not os.path.exists(chemin):
            os.makedirs(chemin)

    @Slot(bool)
    def activer_titre(self, titre_selec: bool):
        if titre_selec:
            self.fen_titre = Fen_Titre()
            self.fen_titre.titre_selectionne.connect(self.recuperer_titre)
            self.fen_titre.exec()   # ouverture de la fenetre

    @Slot(str)
    def recuperer_titre(self, titre_saisi: str):
        print(f"Titre reçu : {titre_saisi}")
        t = Titres(1200, 1380, titre_saisi)
        print("Instance Titres créée")
        t.titre_horizontal()
        print("titre_horizontal exécutée")
        # self.encadrements = t.encadrements_titre()
        # print("encadrements_titre exécutée")
        t.titre_vertical1()
        print("titre_vertical1 exécutée")
        t.titre_vertical2()
        print("titre_vertical2 exécutée")

    @Slot()
    def action_recuperer_tags(self):
        """Récupère les tags depuis le CD et crée tags.txt."""
        lecteur = Path("/media/jerome/CDROM")  # ou "D:/"
        dossier = Path.home() / "PyCDCover"
        self.tags = Tags(lecteur, dossier)
        self.tags.recuperer_tags_cd()
        print("Fichier tags.txt créé dans", dossier)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    appli = Application()
    appli.fenetre.show()  # on affiche la fenêtre principale
    app.exec()