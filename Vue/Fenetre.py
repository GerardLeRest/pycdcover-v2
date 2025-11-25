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
        self.setMaximumSize(1250, 800)
        self.resize(1100, 700)
        self.setWindowFlags(
            Qt.Window
            | Qt.CustomizeWindowHint
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowCloseButtonHint
        )
        # construction de l'interface
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
                background-color: #ffaa43;
                color: white;
            }
        """)
        # icônes
        self.dossier_icones = Path(__file__).resolve().parent.parent / "ressources" / "icones"
        self.act_titre = QAction(QIcon(str(self.dossier_icones / "titre.svg")), "Titre", self)
        self.act_recup_tags = QAction(QIcon(str(self.dossier_icones / "recup_tags.svg")), "Récupérer les tags", self)
        self.act_tags_rw = QAction(QIcon(str(self.dossier_icones / "tags_rw.svg")), "Lire/Écrire tags", self)
        self.act_recup_images = QAction(QIcon(str(self.dossier_icones / "recup_images.svg")), "Récupérer les images", self)
        self.act_faces = QAction(QIcon(str(self.dossier_icones / "deux_faces.svg")), "Générer 2 faces", self)
        self.act_pdf = QAction(QIcon(str(self.dossier_icones / "pdf.svg")), "PDF", self)
        for a in (self.act_titre, self.act_recup_tags, self.act_tags_rw,
                  self.act_recup_images, self.act_faces, self.act_pdf):
            toolbar.addAction(a)
        # info-bulles
        self.act_titre.setToolTip("Créer le titre")
        self.act_recup_tags.setToolTip("Récupérer les tags")
        self.act_tags_rw.setToolTip("Éditer/Modifier les tags")
        self.act_recup_images.setToolTip("Récupérer les images")
        self.act_faces.setToolTip("Créer les deux faces")
        self.act_pdf.setToolTip("Créer le pdf")
        # activation des boutons
        self.act_titre.setEnabled(True)
        for a in (self.act_recup_tags, self.act_tags_rw,
                  self.act_recup_images, self.act_faces, self.act_pdf):
            a.setEnabled(False)
        # Connexions Vue → Contrôleur
        self.act_titre.triggered.connect(self.demande_saisie_titre.emit)
        self.act_recup_tags.triggered.connect(self.demande_ouvrir_recuperation_tags.emit)
        self.act_tags_rw.triggered.connect(self.demande_ouvrir_editeur_tags.emit)
        self.act_recup_images.triggered.connect(self.demande_recuperer_images.emit)
        self.act_faces.triggered.connect(self.demande_faces.emit)
        self.act_pdf.triggered.connect(self.demande_pdf.emit)

    def panneau_gauche(self) -> None:
        """Construit le panneau gauche (liste des albums)."""
        self.recup_donnees = Haut_gauche()
        self.recup_donnees.charger_depuis_fichier()
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
                background-color: #FE6E3E;
                color: white;
                font-weight: 600;
            }
            QListWidget::item:hover {
                background-color: #FFAA43;
                color: white;
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
