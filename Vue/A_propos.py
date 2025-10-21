from PySide6.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QPushButton
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os

class FenetreAPropos(QDialog):

    def __init__(self):
        super().__init__()

        # tailles de la fenêtre
        self.setMinimumSize(250, 250)
        self.setMaximumSize(290, 290)
        self.setWindowTitle("PyCDCover")

        # construction des éléments
        self.preparation_titre()
        self.preparation_texte_haut()
        self.preparation_image()
        self.preparation_texte_bas()
        self.preparation_bouton_fermer()

        # mise en page
        self.layouts()

    def preparation_titre(self) -> None:
        """construction du label du titre"""
        self.titre = QLabel("Auteur : Gérard Le Rest", self)
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

    def preparation_image(self) -> None:
        """construction de l'icône"""
        racine_projet = os.path.dirname(os.path.abspath(__file__))
        racine_projet = os.path.join(racine_projet, "..")
        print(f"racine: {racine_projet}")
        # if racine_projet.endswith("Vue"):
        #     racine_projet = os.path.abspath(os.path.join(racine_projet, ".."))
        # elif racine_projet.endswith("Controleur"):
        #     racine_projet = os.path.abspath(os.path.join(racine_projet, ".."))
        chemin_image = os.path.join(racine_projet, "icones", "icone.png")
        self.label_icone = QLabel()
        pixmap = QPixmap(chemin_image)
        # dimensionner l'image
        pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_icone.setPixmap(pixmap)
        # centrer l'iamge
        self.label_icone.setAlignment(Qt.AlignCenter)
        self.label_icone.setStyleSheet("""
            QLabel {
                padding: 5px;
            }
        """)

    def preparation_texte_bas(self) -> None:
        """construction du label du texte du bas"""
        self.texte_bas = QLabel(
            "Pochettes : https://musicbrainz.org/\n"
            "Matérial icons : https://musicbrainz.org", self
        )
        self.texte_bas.setAlignment(Qt.AlignCenter)
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
                border: 1px solid #E67E22;
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
        layout.addWidget(self.label_icone)
        layout.addWidget(self.texte_bas)
        layout.addSpacing(8)
        layout.addWidget(self.bouton_fermer, alignment=Qt.AlignHCenter)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    w = FenetreAPropos()
    w.show()
    app.exec()

