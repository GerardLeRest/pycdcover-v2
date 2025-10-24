from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem,  QMessageBox
)
from PySide6.QtCore import Qt, QSize, Slot, Signal
from PySide6.QtGui import QIcon, QAction
from pathlib import Path
from .Haut_gauche import Haut_gauche
from .Haut_milieu import Haut_milieu
from .Haut_droit import Haut_droit
from .Bas import Bas
from Modele.Tags import Tags
from Modele.recup_images_avant import lire_tags, TelechargementUI
from Modele.Lancement_av_ar import Lancement_av_ar
from Modele.Gabarit import Gabarit
from .A_propos import FenetreAPropos
import sys, os

class Fenetre(QMainWindow):
    """Fenêtre principale de l'application"""
    # Signal émis quand l’utilisateur clique sur “Titre”
    demande_saisie_titre = Signal(bool)

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
        self.dossier_pycovercd = dossier_utilisateur / "PyCDCover"
        self.dossier_thumbnails = self.dossier_pycovercd / "thumbnails"
        os.chdir(self.dossier_pycovercd)
        # methodes
        self.menu()
        self.barre_d_outils()
        self.panneau_gauche()
        self.panneau_milieu()
        self.panneau_droit()
        self.panneau_bas()
        self.connexions()

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

        # --- Icônes et actions
        self.dossier_icones = Path(__file__).resolve().parent.parent / "icones"
        act_titre = QAction(QIcon(str(self.dossier_icones / "titre.svg")), "Titre", self)
        act_recup_tags = QAction(QIcon(str(self.dossier_icones / "recup_tags.svg")), "Récupérer les tags", self)
        act_tags_rw = QAction(QIcon(str(self.dossier_icones / "tags_rw.svg")), "Lire/écrire tags", self)
        act_recup_images = QAction(QIcon(str(self.dossier_icones / "recup_images.svg")), "Récupérer les images", self)
        act_faces = QAction(QIcon(str(self.dossier_icones / "deux_faces.svg")), "Générer 2 faces", self)
        act_pdf = QAction(QIcon(str(self.dossier_icones / "pdf.svg")), "PDF", self)

        # --- Ajout à la barre d’outils
        for a in (act_titre, act_recup_tags, act_tags_rw, act_recup_images, act_faces, act_pdf):
            toolbar.addAction(a)

        # --- Connexion
         # icone enclenchée lance la méthode action_titre grâce au signal
        act_titre.triggered.connect(self.action_titre)
        act_titre.setToolTip("Créer le titre")

        act_recup_tags.triggered.connect(self.action_recuperer_tags)
        act_tags_rw.triggered.connect(self.action_lire_ecrire_tags)
        act_recup_images.triggered.connect(self.action_recuperer_images)
        act_faces.triggered.connect(self.action_generer_deux_faces)
        act_pdf.triggered.connect(self.action_pdf)

    def panneau_gauche(self) -> None:
        """Construit le panneau gauche (liste des albums)."""
        self.recup_donnees = Haut_gauche()
        self.recup_donnees.charger_depuis_fichier("tags.txt")
        print("tableau chargé:", self.recup_donnees.tableau)

        self.liste = QListWidget()
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
        self.liste.setFixedWidth(300)
        self.liste.addItems(self.recup_donnees.tableau)
        self.liste.itemClicked.connect(self.on_item_clicked)
        self.layout_haut.addWidget(self.liste)

    def panneau_milieu(self) -> None:
        """Construit le panneau central (visuel de l’album)."""
        self.haut_milieu = Haut_milieu("Albert Hammond", "Wonderful, Glourious", "index3.jpeg")
        self.layout_haut.addWidget(self.haut_milieu)

    def panneau_droit(self) -> None:
        """Construit le panneau droit (informations de l’album)."""
        self.haut_droit = Haut_droit("Albert Hammond", "Wonderful, Glorious", "2012", "Rock")
        self.layout_haut.addWidget(self.haut_droit, alignment=Qt.AlignTop)

        self.layout.addLayout(self.layout_haut)
        self.layout.addSpacing(8)

    def panneau_bas(self) -> None:
        """Construit le panneau inférieur (liste des chansons)."""
        chansons = [
            {"numero": 1, "titre": "Tunnel of Love"},
            {"numero": 2, "titre": "Romeo and Juliet"},
            {"numero": 3, "titre": "Skateaway"},
            {"numero": 4, "titre": "Expresso Love"},
            {"numero": 5, "titre": "Hand in Hand"}
        ]
        self.bas = Bas(chansons, "Wonderful", "Dire Straits", "2012")
        self.layout_bas.addWidget(self.bas, alignment=Qt.AlignTop)
        self.layout.addLayout(self.layout_bas)
        self.central.setLayout(self.layout)

    def connexions(self) -> None:
        """Connecte les signaux entre les différents panneaux."""
        self.recup_donnees.album_selectionne.connect(self.haut_milieu.MAJ_haut_milieu)
        self.recup_donnees.album_selectionne.connect(self.haut_droit.MAJ_haut_droit)
        self.recup_donnees.album_selectionne.connect(self.bas.MAJ_bas)

    @Slot(QListWidgetItem)
    def on_item_clicked(self, item: QListWidgetItem) -> None:
        """Met à jour les panneaux quand un album est sélectionné."""
        cle = item.text()
        infos = self.recup_donnees.albums.get(cle)
        if not infos:
            return

        self.recup_donnees.selectionner_album(cle)
        print("   artiste   :", infos.get("artiste"))
        print("   album     :", infos.get("album"))
        print("   annee     :", infos.get("annee"))
        print("   genre     :", infos.get("genre"))
        print("   couverture:", infos.get("couverture"))
        for t in infos.get("chansons", []):
            print("   ", t["numero"], "-", t["titre"])

    @Slot(bool)
    def action_titre(self, checked: bool = False) -> None:
        """Émet le signal de demande de saisie du titre."""
        self.demande_saisie_titre.emit(True) # le signal émet True

    def information(self) -> None:
        """Ouvre la fenêtre 'À propos'."""
        fen_a_propos = FenetreAPropos()
        fen_a_propos.exec()

    def action_recuperer_tags(self) -> None:
        """Récupère les tags à partir du fichier des métadonnées."""
        tags = Tags()
        tags.recuperer_tags()

    def action_lire_ecrire_tags(self) -> None:
        """Lit ou modifie le fichier tags.txt """
        
    def action_recuperer_images(self) -> None:
        albums = lire_tags("tags.txt")
        if not albums:
            QMessageBox.warning(self, "Aucun album trouvé", "Le fichier 'tags.txt' est vide ou introuvable.")
            return

        self.telechargement_ui = TelechargementUI(albums, self.dossier_pycovercd)
        self.telechargement_ui.show()

        
    def action_generer_deux_faces(self) -> None:
        """Génère les deux images de la jaquette (avant et arrière)."""
        lancement_av_ar = Lancement_av_ar()

    def action_pdf(self) -> None:
        """Génère le PDF final à partir des images créées."""
        gabarit = Gabarit(72.0/254,1200,1200,1380,930)
        gabarit.lignes()
        gabarit.insertion_des_images()
        gabarit.trace_rectangles_trait_continu()
        
            
