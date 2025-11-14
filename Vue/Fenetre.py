#!/usr/bin/env python3
"""
Fenetre.py: fenêtre principale de la classe
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QAction
from pathlib import Path
from Vue.Haut_gauche import Haut_gauche
from Vue.Haut_milieu import Haut_milieu
from Vue.Haut_droit import Haut_droit
from Vue.Bas import Bas
from Modele.recup_images_avant import lire_tags
from Vue.A_propos import FenetreAPropos
import sys


class Fenetre(QMainWindow):
    """Fenêtre principale de l'application"""

    # Signaux envoyés vers le contrôleur
    # --- Signaux envoyés vers le contrôleur
    demande_saisie_titre = Signal() # quand on clique sur "Titre"
    demande_ouvrir_recuperation_tags = Signal() # quand on clique sur "Récupérer tags"
    demande_ouvrir_editeur_tags = Signal() # quand on clique sur "Lire/Écrire tags"
    demande_recuperer_images = Signal() # quand on clique sur "Récupérer images"
    demande_faces = Signal() # quand on clique sur "Créer faces"
    demande_pdf = Signal() # quand on clique sur "Créer PDF"
  

    def __init__(self):
        """Initialisation de la fenêtre principale."""
        # ajouter le dossier parent du projet dans les chemins connus
        sys.path.append(str(Path(__file__).resolve().parents[1]))
        super().__init__()
        self.setWindowTitle("PyCDCover")
        # --- Layouts
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout()       # layout global
        self.layout_haut = QHBoxLayout()  # partie supérieure
        self.layout_bas = QVBoxLayout()   # partie inférieure
        # dossiers
        dossier_utilisateur = Path.home()
        self.dossier_pycdcover = dossier_utilisateur / "PyCDCover"
        self.dossier_thumbnails = self.dossier_pycdcover / "thumbnails"
        self.tags_txt = self.dossier_pycdcover / "tags.txt"
        self.editeur_tags = None  # on garde la référence de l'éditeur
        # taillesde la fenetre
        self.setMinimumSize(900, 600)
        self.setMaximumSize(1250, 800)
        self.resize(1100, 700)  # Taille par défaut agréable
        # bloquer le bouton maximiser
        self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        # methodes
        self.menu()
        self.barre_d_outils()
        self.panneau_gauche()
        self.panneau_milieu()
        self.panneau_droit()
        self.panneau_bas()
        self.connexions_donnees()
       
    def menu(self) -> None:
        """Construit le menu principal."""
        barre = self.menuBar()
        menu_aide = barre.addMenu("Aide")
        action_a_propos = QAction("À propos", self)
        action_a_propos.triggered.connect(self.information)
        menu_aide.addAction(action_a_propos)

    def barre_d_outils(self) -> None:
        """Construit la barre d’outils principale avec ses icônes et ses actions."""
        toolbar = QToolBar("Icônes")
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(toolbar)
        toolbar.setStyleSheet("""
            QToolButton:hover {
                background-color: #ffaa43; /* orange sur survol */
                color: white;
            }
        """)
        # --- Dossier des icônes
        self.dossier_icones = Path(__file__).resolve().parent.parent / "ressources" / "icones"
        # --- Création des actions
        self.act_titre = QAction(QIcon(str(self.dossier_icones / "titre.svg")), "Titre", self)
        self.act_recup_tags = QAction(QIcon(str(self.dossier_icones / "recup_tags.svg")), "Récupérer les tags", self)
        self.act_tags_rw = QAction(QIcon(str(self.dossier_icones / "tags_rw.svg")), "Lire/Écrire tags", self)
        self.act_recup_images = QAction(QIcon(str(self.dossier_icones / "recup_images.svg")), "Récupérer les images", self)
        self.act_faces = QAction(QIcon(str(self.dossier_icones / "deux_faces.svg")), "Générer 2 faces", self)
        self.act_pdf = QAction(QIcon(str(self.dossier_icones / "pdf.svg")), "PDF", self)
        # --- Ajout à la barre d’outils
        for a in (self.act_titre, self.act_recup_tags, self.act_tags_rw, self.act_recup_images, self.act_faces, self.act_pdf):
            toolbar.addAction(a)
        # Bulls d'information
        self.act_titre.setToolTip("Créer le titre")
        self.act_recup_tags.setToolTip("Récupérer les tags")
        self.act_tags_rw.setToolTip("Éditer/Modifier les tags")
        self.act_recup_images.setToolTip("Récupérer les images")
        self.act_faces.setToolTip("Créer les deux faces")
        self.act_pdf.setToolTip("Créer le pdf")
         # activer le bouton "Titre"
        self.act_titre.setEnabled(True)
        # désactiver tous les autres boutons
        for a in (self.act_recup_tags, self.act_tags_rw,
                self.act_recup_images, self.act_faces, self.act_pdf):
            a.setEnabled(False)
        
        # Connexions Vue → Controle
        self.act_titre.triggered.connect(self.demande_saisie_titre.emit)
        self.act_recup_tags.triggered.connect(self.demande_ouvrir_recuperation_tags.emit)
        self.act_tags_rw.triggered.connect(self.demande_ouvrir_editeur_tags.emit)
        self.act_recup_images.triggered.connect(self.demande_recuperer_images.emit)
        self.act_faces.triggered.connect(self.demande_faces.emit)
        self.act_pdf.triggered.connect(self.demande_pdf.emit)


    def panneau_gauche(self) -> None:
        """Construit le panneau gauche (liste des albums)."""
        self.recup_donnees = Haut_gauche()
        # chemin correct du fichier tags.txt
        chemin_tags = self.tags_txt
        self.recup_donnees = Haut_gauche()
        self.recup_donnees.charger_depuis_fichier()  
        print("tableau chargé:", self.recup_donnees.tableau)
        print("tableau chargé:", self.recup_donnees.tableau)
        self.liste = QListWidget()
        self.liste.setStyleSheet("""
            QListWidget {
                font-size: 16px;
                color: #6b5e4f;
                margin: 15px;
                border: 1px solid #d3d3d3;
                background-color: white;
            }
            QListWidget::item {
                padding: 6px 10px;
                margin: 2px 4px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                border: none;
                outline: none;
                background-color: #FE6E3E;   /* orange rouge cohérent */
                color: white;
                font-weight: 600;
            }
            QListWidget::item:hover {
                background-color: #FFAA43;
                color: white;
            }
        """)
        self.liste.setFocusPolicy(Qt.NoFocus)
        self.liste.viewport().setStyleSheet("outline: none; border: none; background: transparent;")
        self.liste.setFixedWidth(300)
        self.liste.addItems(self.recup_donnees.tableau)
        self.liste.itemClicked.connect(self.on_item_clicked)
        self.layout_haut.addWidget(self.liste)  

    
    def panneau_milieu(self) -> None:
        """Construit le panneau central (visuel de l’album)."""
        self.haut_milieu = Haut_milieu("", "", "")
        self.layout_haut.addWidget(self.haut_milieu)
        self.haut_milieu.assembler_elements()


    def panneau_droit(self) -> None:
        """Construit le panneau droit (informations de l’album)."""
        self.haut_droit = Haut_droit("", "", "","")
        self.layout_haut.addWidget(self.haut_droit, alignment=Qt.AlignTop)

        self.layout.addLayout(self.layout_haut)
        self.layout.addSpacing(8)

    def panneau_bas(self) -> None:
        """Construit le panneau inférieur (liste des chansons)."""
        chansons = [
            {"numero": 1, "titre": "T"},
            {"numero": 2, "titre": ""},
            {"numero": 3, "titre": ""},
            {"numero": 4, "titre": ""},
            {"numero": 5, "titre": ""}
        ]
        self.bas = Bas([], "", "", "")
        self.layout_bas.addWidget(self.bas, alignment=Qt.AlignTop)
        self.layout.addLayout(self.layout_bas)
        self.central.setLayout(self.layout)

    def connexions_donnees(self) -> None:
        """Connecte les signaux entre les différents panneaux."""
        self.recup_donnees.album_selectionne.connect(self.haut_milieu.MAJ_haut_milieu)
        self.recup_donnees.album_selectionne.connect(self.haut_droit.MAJ_haut_droit)
        self.recup_donnees.album_selectionne.connect(self.bas.MAJ_bas)

    def on_item_clicked(self, item: QListWidgetItem)->None:
        """méthode lancée suite à un clic sur un élément de la liste"""
        cle = item.text()
        print("Clic sur :", cle)
        # récupération des infos
        infos = self.recup_donnees.albums.get(cle)
        if not infos:        
            return
        self.recup_donnees.album_selectionne.emit(infos)  # émémission de infos

        # affichage des différentes données
        print("   artiste   :", infos.get("artiste"))
        print("   album     :", infos.get("album"))
        print("   annee     :", infos.get("annee"))
        print("   genre     :", infos.get("genre"))
        print("   couverture:", infos.get("couverture"))
        for t in infos.get("chansons", []):
            print("   ", t["numero"], "-", t["titre"])

    def information(self) -> None:
        """Ouvre la fenêtre 'À propos'."""
        fen_a_propos = FenetreAPropos()
        fen_a_propos.exec()