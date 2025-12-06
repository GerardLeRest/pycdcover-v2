#!/usr/bin/env python3
"""
Fenetre.py: fenêtre principale de la classe
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QAction
from pathlib import Path
from Vue.Haut_gauche import Haut_gauche
from Vue.Haut_milieu import Haut_milieu
from Vue.Haut_droit import Haut_droit
from Vue.Bas import Bas
from Vue.A_propos import FenetreAPropos
import sys
from Vue.utils import centrer_fenetre


class Fenetre(QMainWindow):
    """Fenêtre principale de l'application"""

    demande_saisie_titre = Signal()
    demande_ouvrir_recuperation_tags = Signal()
    demande_ouvrir_editeur_tags = Signal()
    demande_recuperer_images = Signal()
    demande_faces = Signal()
    demande_pdf = Signal()

    def __init__(self):
        """Initialisation de la fenêtre principale."""
        sys.path.append(str(Path(__file__).resolve().parents[1]))
        super().__init__()
        self.setWindowTitle("PyCDCover")
        # layouts principaux
        self.central = QWidget()
        self.setCentralWidget(self.central)
        self.layout = QVBoxLayout()
        self.layout_haut = QHBoxLayout()
        self.layout_bas = QVBoxLayout()
        # dossiers
        dossier_utilisateur: Path = Path.home()
        self.dossier_pycdcover: Path = dossier_utilisateur / "PyCDCover"
        self.dossier_thumbnails: Path = self.dossier_pycdcover / "thumbnails"
        self.tags_txt: Path = self.dossier_pycdcover / "tags.txt"
        # tailles de la fenêtre
        self.setMinimumSize(900, 600)
        self.setMaximumSize(1000, 720)
        self.resize(1100, 700)
        self.setWindowFlags(
            Qt.Window
            | Qt.CustomizeWindowHint
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowCloseButtonHint
        )
        # déclaration des actions
        self.act_titre = QAction("Titre", self)
        self.act_recup_tags = QAction("Récupérer_tags", self)
        self.act_tags_rw = QAction("Lire/Écrire tags", self)
        self.act_recup_images = QAction("Récupérer les images", self)
        self.act_faces = QAction("Créer les deux faces", self)
        self.act_pdf = QAction("Générer le pdF", self)
        self.act_quitter = QAction("Quitter")

        # Connexions communes
        self.act_titre.triggered.connect(self.demande_saisie_titre.emit)
        self.act_recup_tags.triggered.connect(self.demande_ouvrir_recuperation_tags.emit)
        self.act_tags_rw.triggered.connect(self.demande_ouvrir_editeur_tags.emit)
        self.act_recup_images.triggered.connect(self.demande_recuperer_images.emit)
        self.act_faces.triggered.connect(self.demande_faces.emit)
        self.act_pdf.triggered.connect(self.demande_pdf.emit)
        self.act_quitter = QAction(QIcon("ressources/icones/quitter.svg"), "Quitter", self)
        self.act_quitter.triggered.connect(self.close)

        # État initial
        self.act_titre.setEnabled(True)
        self.act_recup_tags.setEnabled(False)
        self.act_tags_rw.setEnabled(False)
        self.act_recup_images.setEnabled(False)
        self.act_faces.setEnabled(False)
        self.act_pdf.setEnabled(False)
        self.act_quitter.setEnabled(True)

        # construction de l'interface
        self.menu()
        self.barre_d_outils()
        self.panneau_gauche()
        self.panneau_milieu()
        self.panneau_droit()
        self.panneau_bas()
        self.connexions_donnees()
        # voir le fichier utilis.py dans Vue
        centrer_fenetre(self) 

    def menu(self) -> None:
        """Construit le menu principal."""
        barre = self.menuBar()
        # menu fichiers
        menu_fichiers =barre.addMenu("Fichier")
        menu_fichiers.addAction(self.act_titre)
        menu_fichiers.addAction(self.act_recup_tags)
        menu_fichiers.addSeparator()
        menu_fichiers.addAction(self.act_tags_rw)
        menu_fichiers.addSeparator()
        menu_fichiers.addAction(self.act_recup_images)
        menu_fichiers.addAction(self.act_faces)
        menu_fichiers.addAction(self.act_pdf)
        menu_fichiers.addAction(self.act_quitter)
        #menu aide
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
                background-color: #ffaa43;
                color: white;
            }
        """)
        # dossier des icones
        self.dossier_icones = Path(__file__).resolve().parent.parent / "ressources" / "icones"

        # On ajoute des icônes aux **actions déjà existantes**
        self.act_titre.setIcon(QIcon(str(self.dossier_icones / "titre.svg")))
        self.act_recup_tags.setIcon(QIcon(str(self.dossier_icones / "recup_tags.svg")))
        self.act_tags_rw.setIcon(QIcon(str(self.dossier_icones / "tags_rw.svg")))
        self.act_recup_images.setIcon(QIcon(str(self.dossier_icones / "recup_images.svg")))
        self.act_faces.setIcon(QIcon(str(self.dossier_icones / "deux_faces.svg")))
        self.act_pdf.setIcon(QIcon(str(self.dossier_icones / "pdf.svg")))
        
        # ajout des actions
        toolbar.addAction(self.act_titre)
        toolbar.addAction(self.act_recup_tags)
        toolbar.addAction(self.act_tags_rw)
        toolbar.addAction(self.act_recup_images)
        toolbar.addAction(self.act_faces)
        toolbar.addAction(self.act_pdf)

        # info-bulles
        self.act_titre.setToolTip("Créer le titre")
        self.act_recup_tags.setToolTip("Récupérer les tags")
        self.act_tags_rw.setToolTip("Éditer/Modifier les tags")
        self.act_recup_images.setToolTip("Récupérer les images")
        self.act_faces.setToolTip("Créer les deux faces")
        self.act_pdf.setToolTip("Créer le pdf")
       
    def panneau_gauche(self) -> None:
        """Construit le panneau gauche (liste des albums)."""
        self.recup_donnees = Haut_gauche()
        self.recup_donnees.charger_depuis_fichier()
        self.liste = QListWidget()
        self.setStyleSheet("""
            /* LISTE GLOBALE */
            QListWidget {
                font-size: 16px;            
                color: #4a4036;                 /* texte plus lisible et plus moderne */
                margin: 15px;
                border: 1px solid #d7d7d7;      /* bordure plus élégante, moins brute */
                background-color: #fafafa;      /* gris très clair pro */
            }

            /* ITEMS */
            QListWidget::item {
                padding: 6px 10px;
                margin: 2px 4px;
                border-radius: 4px;
            }

            /* SÉLECTION (version assourdie, look pro) */
            QListWidget::item:selected {
                background-color: #e89b3f;      /* orange doux, moins "flashy" */
                color: white;
                font-weight: 600;
            }

            /* HOVER (subtil, élégant) */
            QListWidget::item:hover {
                background-color: #f2c792;      /* beige orangé très doux */
                color: #fff;
            }
    """)
        self.liste.setFocusPolicy(Qt.NoFocus)
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
        self.haut_droit = Haut_droit("", "", "", "")
        self.layout_haut.addWidget(self.haut_droit, alignment=Qt.AlignTop)
        self.layout.addLayout(self.layout_haut)
        self.layout.addSpacing(8)

    def panneau_bas(self) -> None:
        """Construit le panneau inférieur (liste des chansons)."""
        self.bas = Bas([], "", "", "")
        self.layout_bas.addWidget(self.bas, alignment=Qt.AlignTop)
        self.layout.addLayout(self.layout_bas)
        self.central.setLayout(self.layout)

    def connexions_donnees(self) -> None:
        """Connecte les signaux entre les différents panneaux."""
        self.recup_donnees.album_selectionne.connect(self.haut_milieu.MAJ_haut_milieu)
        self.recup_donnees.album_selectionne.connect(self.haut_droit.MAJ_haut_droit)
        self.recup_donnees.album_selectionne.connect(self.bas.MAJ_bas)

    def on_item_clicked(self, item: QListWidgetItem) -> None:
        """Réagit au clic sur un album dans la liste."""
        cle = item.text()
        infos = self.recup_donnees.albums.get(cle)
        if not infos:
            return
        self.recup_donnees.album_selectionne.emit(infos)

    def information(self) -> None:
        """Ouvre la fenêtre 'À propos'."""
        fen_a_propos = FenetreAPropos()
        fen_a_propos.exec()
