#!/usr/bin/env python3
"""
A_propose.py - fenêtre d'informations du programme
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os

class FenetreAPropos(QDialog):
    """fentetre d'information sur le logiciel"""
    
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: #fffdf8;")
        # tailles de la fenêtre
        self.setMinimumSize(330, 450)
        self.setMaximumSize(550, 550)
        self.setWindowTitle("PyCDCover")
        # chemin des images:
        self.racine_fichier = os.path.dirname(os.path.abspath(__file__))
        self.racine_projet = os.path.join(self.racine_fichier, "..")
        #self.label_icone
        # construction des éléments
        self.preparation_titre()
        self.preparation_texte_haut()
        self.label_image = self.preparation_image(self.racine_projet, 120, 120, "icone")
        self.preparation_texte_bas()
        self.preparation_bouton_fermer()
        self.label_icone = self.preparation_image(self.racine_projet, 48, 48, "petite_icone")
        # mise en page
        self.layouts()

    def preparation_titre(self) -> None:
        """construction du label du titre"""
        self.titre = QLabel("PyCDCover - v0.9", self)
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
        self.texte_haut = QLabel("Licence : GNU GPL v3\n2015 - 2025", self)
        self.texte_haut.setAlignment(Qt.AlignCenter)
        self.texte_haut.setStyleSheet("""
            QLabel {
                color: #333;
                font-size: 11pt;
                text-align: center;
            }
        """)

    def preparation_image(self, chemin, x, y, nom_image) -> None:
        """construction de l'icône"""
        chemin = os.path.join(self.racine_projet, "icones", nom_image)
        label = QLabel("",self)
        pixmap = QPixmap(chemin)  # Chargement de l'image
        # dimensionner l'image
        pixmap = pixmap.scaled(x, y, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(pixmap)
        # centrer l'iamge
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                padding: 5px;
            }                                    
        """)
        return label

    def preparation_texte_bas(self) -> None:
        """construction du label du texte du bas"""
        self.texte_bas = QLabel(
            "Images : <a href='https://pixabay.com/fr/'>pixabay.com</a><br>"
            "Material icons : <a href='https://musicbrainz.org'>musicbrainz.org</a><br>"
            "Chemin des fichiers :<br>"
            "GNU/Linux : ~/PyCDCover/<br>"
            "macOS : ~/PyCDCover/<br>"
            "Windows : C:/Users/Nom_utilisateur/PyCDCover/<br>"
            "Auteur : <b>Gérard LE REST </b> - "
            "Site : <a href='https://gerardlerest.github.io/soignemoi/'>soignemoi</a><br>"
            "Contact : <a href='mailto:ge.lerest@gmail.com'>ge.lerest@gmail.com</a><br>",
            self
        )
        self.texte_bas.setOpenExternalLinks(True)  # 🔗 rend les liens cliquables
        # permet de cliquer sans sélection de texte.
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
        self.bouton_fermer = QPushButton("Fermer", self)
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
        layout.addWidget(self.label_icone)

        self.setLayout(layout)
        self.show()

# ------------------------------------------------------------------------------
# Programme principal de test
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication([])
    w = FenetreAPropos()
    app.exec()

