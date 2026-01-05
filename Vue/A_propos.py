#!/usr/bin/env python3
"""
A_propos.py - fenêtre d'informations du programme
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os
from pathlib import Path
from Vue.utils import centrer_fenetre # fonction
from builtins import _

class FenetreAPropos(QDialog):
    """fentetre d'information sur le logiciel"""
    
    def __init__(self):
        """initialisation"""
        super().__init__()
        self.setStyleSheet("background-color: #fffdf8;")
        # tailles de la fenêtre
        self.setMinimumSize(330, 450)
        self.setMaximumSize(550, 550)
        self.setWindowTitle("PyCDCover")
        self.titre: QLabel | None = None
        self.texte_haut: QLabel | None = None
        self.texte_bas: QLabel | None = None
        self.bouton_fermer: QPushButton | None = None
        self.label_image: QLabel | None = None
        # chemin des images:
        self.racine_fichier: Path = Path(__file__).resolve().parent # .../Vue
        self.racine_projet: Path = self.racine_fichier.parent # .../pycdcover-v2
        # construction des éléments
        self.preparation_titre()
        self.preparation_texte_haut()
        fichier_image = self.racine_projet / "ressources" / "icones" / "icone_128x128.png"
        self.label_image = self.preparation_image(128, 128, fichier_image)
        self.preparation_texte_bas()
        self.preparation_bouton_fermer()
        # mise en page
        self.layouts() 
         # voir le fichier utilis.py dans Vue
        centrer_fenetre(self) 
        
    def preparation_titre(self) -> None:
        """construction du label du titre"""
        self.titre = QLabel(_("PyCDCover"), self)
        self.titre.setAlignment(Qt.AlignCenter)
        self.titre.setStyleSheet("""
            QLabel {
                color: #ffaa43;
                font-size: 18px;
                font-weight: bold;
                text-align: center;
            }
        """)

    def preparation_texte_haut(self) -> None:
        """construction du label du texte du haut"""
        self.texte_haut = QLabel(_("Licence : GNU GPL V2.0.0\n2015 - 2025"), self)
        self.texte_haut.setAlignment(Qt.AlignCenter)
        self.texte_haut.setStyleSheet("""
            QLabel {
                color: #333;
                font-size: 11pt;
                text-align: center;
            }
        """)

    def preparation_image(self,x:int, y:int, nom_image:str) -> QLabel:
        """construction de l'icône"""
        chemin_image = self.racine_projet / "ressources" / "icones" / nom_image
        label = QLabel("", self)
        pixmap = QPixmap(chemin_image)
        pixmap = pixmap.scaled(x, y, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                padding: 5px;
            }
        """)
        return label

    def preparation_texte_bas(self) -> None:
        """construction du label du texte du bas"""
        self.texte_bas = QLabel(_(
            "Images : <a href='https://musicbrainz.org'>musicbrainz.org</a><br>"
            "ou : <a href='https://www.apple.com/fr/itunes/'>Itunes</a><br>"
            "Chemin des fichiers :<br>"
            "GNU/Linux : ~/PyCDCover/<br>"
            "macOS : ~/PyCDCover/<br>"
            "Windows : C:/Users/Nom_utilisateur/PyCDCover/<br>"
            "<br>"
            "Auteur : <b>Gérard LE REST </b> - "
            "Site : <a href='https://gerardlerest.github.io/pycdcover/'>PyCDCover</a><br>"
            "Contact : <a href='mailto:ge.lerest@gmail.com'>ge.lerest@gmail.com</a><br>"),
            self
        )
        self.texte_bas.setOpenExternalLinks(True)
        self.texte_bas.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.texte_bas.setAlignment(Qt.AlignLeft)
        self.texte_bas.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 10pt;
                text-align: center;
            }
        """)

    def preparation_bouton_fermer(self) -> None:
        """construction du bouton Fermer"""
        self.bouton_fermer = QPushButton(_("Fermer"), self)
        self.bouton_fermer.setFixedSize(100, 30)
        self.bouton_fermer.setStyleSheet("""
            QPushButton {
                color: #4e3728;
                border: 1px solid #D3D3D3;
                border-radius: 8px;
                padding: 6px 16px;
                background-color: white;
                font-weight: normal;
            }
            QPushButton:hover {
                background-color: #E67E22;
                color: white;
            }
        """)
        self.bouton_fermer.clicked.connect(self.close)

    def layouts(self):
        """mise en page des éléments"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(5)
        layout.addWidget(self.titre)
        layout.addWidget(self.texte_haut)
        layout.addWidget(self.label_image)
        layout.addWidget(self.texte_bas)
        layout.addSpacing(8)
        layout.addWidget(self.bouton_fermer, alignment=Qt.AlignHCenter)
        # référence à la fenêtre)
        self.setLayout(layout)
        # affichage de la fenêtre
        self.show()


# ------------------------------------------------------------------------------
# Programme principal de test
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication([])
    w = FenetreAPropos()
    app.exec()
