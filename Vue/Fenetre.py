#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyCDCover – Générateur de jaquettes de CD audio
Auteur : Gérard LE REST
Licence : GNU GPL v3
© Gérard LE REST
email: gerard.lerest@orange.fr
Créé en : 01-04-2010
Dernière mise à jour : 2025-10-18
"""

from PySide6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QListWidget, QListWidgetItem, QVBoxLayout, QToolBar, QWidget
import sys
from PySide6.QtCore import Qt, QSize, Slot, Signal
from PySide6.QtGui import QIcon, QAction
from pathlib import Path
from .Haut_gauche import Haut_gauche
from .Haut_milieu import Haut_milieu
from .Haut_droit import Haut_droit
from .Bas import Bas


class Fenetre(QMainWindow):  # QMainWindow plus évolué - plus d'éléments que QWidget

    titre_selectionne = Signal(bool)  # Le signal enverra un booleen

    def __init__(self):
        super().__init__()
        """initialisation"""
        self.setWindowTitle("PyCDCover")
        # icones
        toolbar = QToolBar("Icones")
        toolbar.setIconSize(QSize(32, 32))
        # sert à attacher la barre d’outils à la zone supérieure
        self.addToolBar(toolbar)
        # créer une action avec une icone et un texte
        self.dossier_icones = Path(__file__).resolve().parent.parent / "icones"
        act_titre   = QAction(QIcon(str(self.dossier_icones / "titre.svg")), "Titre", self)
        act_recup   = QAction(QIcon(str(self.dossier_icones / "recup_infos.svg")), "Récupérer tags et images", self)
        act_tags_rw = QAction(QIcon(str(self.dossier_icones / "tags_rw.svg")), "Lire/écrire tags", self)
        act_faces   = QAction(QIcon(str(self.dossier_icones / "deux_faces.svg")), "Générer 2 faces", self)
        act_pdf     = QAction(QIcon(str(self.dossier_icones / "pdf.svg")), "PDF", self)

        # ajout à la barre d'outil sous forme de bouton cliquable
        for a in (act_titre, act_recup, act_tags_rw, act_faces, act_pdf):
            toolbar.addAction(a)

        # connection entre les icones et les définitions + tooltips
        act_titre.triggered.connect(self.action_titre)
        act_titre.setToolTip("Créer le titre")
        act_recup.triggered.connect(self.action_recuperer_tags_images)
        act_recup.setToolTip("récupérer les tags et les images")
        act_tags_rw.triggered.connect(self.action_lire_ecrire_tags)
        act_tags_rw.setToolTip("Lire/modifier le fichier des tags")  # tooltip
        act_faces.triggered.connect(self.action_generer_deux_faces)   # FaceAvant puis FaceArriere
        act_faces.setToolTip("générer les images des deux faces")
        act_pdf.triggered.connect(self.action_pdf)
        act_pdf.setToolTip("générer le pdf")

        # --- IMPORTANT : widget central - on a changé de parent de la fenêtre de QWidget à QMainWindow
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()       # layout de la fenêtre
        layout_haut = QHBoxLayout()  # layout des panneaux du haut
        layout_bas  = QVBoxLayout()  # layout du panneau du bas (chansons)

        # panneau du haut
        # partie haut gauche
        # 1) Instancier le récupérateur ET charger les données AVANT d'ajouter les items
        self.recup_donnees = Haut_gauche()
        self.recup_donnees.charger_depuis_fichier("tags.txt")
        print("tableau chargé:", self.recup_donnees.tableau)

        # 2) Liste des albums
        self.liste = QListWidget()  # liste des albums
        self.liste.setStyleSheet("""
            QListWidget {
                font-size: 16px;
                color: #4e3728;
                margin:15;
            }
            QListWidget::item {
                padding: 4px;
                margin: 4px 6px;
            }
        """)
        # 3) Figer la largeur pour le panneau gauche (stoppe toute variation de layout)
        self.liste.setFixedWidth(300)
        self.liste.addItems(self.recup_donnees.tableau)  # ajouter après chargement
        self.liste.itemClicked.connect(self.on_item_clicked)
        layout_haut.addWidget(self.liste)

        # milieu (on garde une référence pour pouvoir le mettre à jour plus tard)
        haut_milieu = Haut_milieu("Albert Hammond", "Wonderful, Glourious", "index3.jpeg")
        layout_haut.addWidget(haut_milieu)

        # partie droite haute (idem : garder la référence)
        haut_droit = Haut_droit("Albert Hammond", "Wonderful, Glorious", "2012", "Rock")
        layout_haut.addWidget(haut_droit, alignment=Qt.AlignTop)

        layout.addLayout(layout_haut)
        layout.addSpacing(8)

        # panneau du bas
        chansons = [
            {"numero": 1, "titre": "Tunnel of Love"},
            {"numero": 2, "titre": "Romeo and Juliet"},
            {"numero": 3, "titre": "Skateaway"},
            {"numero": 4, "titre": "Expresso Love"},
            {"numero": 5, "titre": "Hand in Hand"}
        ]
        bas = Bas(chansons, "Wonderful", "Dire Straits", "2012")
        layout_bas.addWidget(bas, alignment=Qt.AlignTop)
        layout.addLayout(layout_bas)

        # lier le layout global à la fenêtre
        central.setLayout(layout)

        # connection entre le signal et les slots
        self.recup_donnees.album_selectionne.connect(haut_milieu.MAJ_haut_milieu)
        self.recup_donnees.album_selectionne.connect(haut_droit.MAJ_haut_droit)
        self.recup_donnees.album_selectionne.connect(bas.MAJ_bas)

    @Slot(QListWidgetItem)
    def on_item_clicked(self, item: QListWidgetItem) -> None:
        """Quand un album est cliqué dans la liste."""
        cle = item.text()
        infos = self.recup_donnees.albums.get(cle)
        if not infos:
            return

        # Version stable : appel direct vers le store (Haut_gauche)
        self.recup_donnees.selectionner_album(cle)

        # Affichage debug
        print("   artiste   :", infos.get("artiste"))
        print("   album     :", infos.get("album"))
        print("   annee     :", infos.get("annee"))
        print("   genre     :", infos.get("genre"))
        print("   couverture:", infos.get("couverture"))
        for t in infos.get("chansons", []):
            print("   ", t["numero"], "-", t["titre"])

    @Slot(bool)
    def action_titre(self) -> None:
        self.titre_selectionne.emit(True)

    def action_lire_ecrire_tags(self) -> None:
        """ouvrir/éditer le fichier tags.txt (dialogue + lecture/écriture)"""
        print("lire et écrire tags")

    def action_pdf(self) -> None:
        """générer le PDF final"""
        print("générer pdf")

    def action_generer_deux_faces(self) -> None:
        """enchaîner FaceAvant puis FaceArriere"""
        print("générer les faces avant et arrière de la jaquette")

    def action_recuperer_tags_images(self) -> None:
        """importer/extraire les tags et rafraîchir self.liste"""
        print("importer les tags")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = Fenetre()
    fenetre.show()
    app.exec()

