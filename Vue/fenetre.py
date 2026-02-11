#!/usr/bin/env python3
"""
Fenetre.py: fenêtre principale de la classe
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QMenu, QMessageBox
)
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QAction, QActionGroup
from pathlib import Path
from Vue.haut_gauche import Haut_gauche
from Vue.haut_milieu import Haut_milieu
from Vue.haut_droit import Haut_droit
from Vue.bas import Bas
from Vue.a_propos import FenetreAPropos
from Modele.GestionLangue import GestionLangue
import sys
from Vue.centrer_fenetre import CentrerFenetre
from builtins import _


class Fenetre(QMainWindow):
    """Fenêtre principale de l'application"""
    # signaux
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
        self.dossier_miniatures: Path = self.dossier_pycdcover / "miniatures"
        self.tags_txt: Path = self.dossier_pycdcover / "tags.txt"
        self.fichierLangue: Path = dossier_utilisateur / ".config" / "pycdcover" / "configurationLangue.json"
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
        self.act_titre = QAction(_("Titre"), self)
        self.act_recup_tags = QAction(_("Récupérer les tags"), self)
        self.act_tags_rw = QAction(_("Lire/Écrire tags"), self)
        self.act_recup_images = QAction(_("Récupérer les images"), self)
        self.act_faces = QAction(_("Créer les deux faces"), self)
        self.act_pdf = QAction(_("Générer le PDF"), self)
        self.act_quitter = QAction(_("Quitter"))

        # Connexions communes
        self.act_titre.triggered.connect(self.demande_saisie_titre.emit)
        self.act_recup_tags.triggered.connect(self.demande_ouvrir_recuperation_tags.emit)
        self.act_tags_rw.triggered.connect(self.demande_ouvrir_editeur_tags.emit)
        self.act_recup_images.triggered.connect(self.demande_recuperer_images.emit)
        self.act_faces.triggered.connect(self.demande_faces.emit)
        self.act_pdf.triggered.connect(self.demande_pdf.emit)
        self.act_quitter = QAction(QIcon("ressources/icones/quitter.svg"), _("Quitter"), self)
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
        CentrerFenetre(self) 

    def menu(self) -> None:
        """Construit le menu principal."""
        barre = self.menuBar()
        # menu fichiers
        menu_fichiers = QMenu(_("Fichier"), self)
        barre.addMenu(menu_fichiers)
        menu_fichiers.addAction(self.act_titre)
        menu_fichiers.addAction(self.act_recup_tags)
        menu_fichiers.addAction(self.act_tags_rw)
        menu_fichiers.addAction(self.act_recup_images)
        menu_fichiers.addAction(self.act_faces)
        menu_fichiers.addAction(self.act_pdf)
        menu_fichiers.addSeparator()
        # action des langues
        menu_langues = QMenu(_("Langue"), self)
        groupe_langue = QActionGroup(self)
        groupe_langue.setExclusive(True)
        # récupération de la langue (voir dossier config) 
        self.gestionLangue = GestionLangue(self.fichierLangue) 
        self.actionBrezhoneg = QAction("Brezhoneg", self, checkable=True)
        self.actionBrezhoneg.triggered.connect(lambda: self.changerLangue("br"))
        self.actionEnglish = QAction("English", self, checkable=True)
        self.actionEnglish.triggered.connect(lambda: self.changerLangue("en"))
        self.actionEspagnol = QAction("Español", self, checkable=True)
        self.actionEspagnol.triggered.connect(lambda: self.changerLangue("es"))
        self.actionFrancais = QAction("Français", self, checkable=True)
        self.actionFrancais.triggered.connect(lambda: self.changerLangue("fr"))
        langue = self.gestionLangue.lire()
        self.recuperation_code_langue(langue)
        # lier acions au menu et ay groupe langue
        for action in (self.actionBrezhoneg, self.actionEnglish, self.actionEspagnol,
                       self.actionFrancais):
            groupe_langue.addAction(action)
            menu_langues.addAction(action)
        # "sousMenuLangues" -> menu menuPrincipal
        menu_fichiers.addMenu(menu_langues)
        menu_fichiers.addSeparator()
        menu_fichiers.addAction(self.act_quitter)
        # lier le menu menu fichiers au menuBar
        barre.addMenu(menu_fichiers)
        #menu aide
        menu_aide = barre.addMenu(_("Aide"))
        action_a_propos = QAction(_("À propos"), self)
        action_a_propos.triggered.connect(self.information)
        menu_aide.addAction(action_a_propos)

    def recuperation_code_langue(self, langue)->None:
        "Récupérer le code de la langue"
        if langue == "br":
            self.actionBrezhoneg.setChecked(True)
        elif langue == "en":
            self.actionEnglish.setChecked(True)
        elif langue == "es":
            self.actionEspagnol.setChecked(True)
        else:
            self.actionFrancais.setChecked(True)    
    
    def changerLangue(self, codeLangue)->None:
        """changer la langue"""
        self.gestionLangue.ecrire(codeLangue)
        # sélection du radio
        self.afficherMessage()

    def afficherMessage(self)->None:
        "afficher le message d'avertissement"
        QMessageBox.warning(
            self,
            _("Attention"),
            _("Les changements prendront effet au prochain démarrage.")
        )

    def barre_d_outils(self) -> None:
        """Construit la barre d’outils principale avec ses icônes et ses actions."""
        barre_outils = QToolBar("Icônes")
        barre_outils.setIconSize(QSize(32, 32))
        self.addToolBar(barre_outils)
        barre_outils.setStyleSheet("""
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
        barre_outils.addAction(self.act_titre)
        barre_outils.addAction(self.act_recup_tags)
        barre_outils.addAction(self.act_tags_rw)
        barre_outils.addAction(self.act_recup_images)
        barre_outils.addAction(self.act_faces)
        barre_outils.addAction(self.act_pdf)

        # info-bulles
        self.act_titre.setToolTip(_("Créer le titre"))
        self.act_recup_tags.setToolTip(_("Récupérer les tags"))
        self.act_tags_rw.setToolTip(_("Éditer/Modifier les tags"))
        self.act_recup_images.setToolTip(_("Récupérer les images"))
        self.act_faces.setToolTip(_("Créer les deux faces"))
        self.act_pdf.setToolTip(_("Générer le PDF"))
       
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
