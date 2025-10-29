from PySide6.QtWidgets import (QMainWindow, QPushButton, QTextEdit, QLabel,
                               QVBoxLayout, QHBoxLayout, QWidget, QApplication)
from PySide6.QtCore import Qt
from pathlib import Path
import sys


class Editeur_tags(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Éditeur de tags")
        self.resize(300, 400)
        # Chemin du fichier tags.txt
        self.chemin_tags = Path.home() / "PyCDCover" / "tags.txt"
        self.interface()
    
    def interface(self):
        """interaction enttre les bouton et l'éditeur"""
        # layouts principal
        layout = QVBoxLayout()
        # Zone de texte
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)
         # Charger le contenu au démarrage
        self.charger_tags()
        #Layout horizontal
        layout_hor = QHBoxLayout()
        #bouton valider
        valider = QPushButton("valider", self) 
        valider.setFixedWidth(100)
        layout_hor.addWidget(valider)
        self.habillage_bouton(valider)
        valider.clicked.connect(self.quitter_sauvegarder)
        # bouton abandonner
        abandonner = QPushButton("Quitter", self)
        abandonner.setFixedWidth(100)
        self.habillage_bouton(abandonner)
        abandonner.clicked.connect(self.quitter_sans_enregistrer)
        layout_hor.addWidget(abandonner, alignment=Qt.AlignRight)
        # layouts
        layout.addLayout(layout_hor)
        conteneur = QWidget()
        conteneur.setLayout(layout)
        self.setCentralWidget(conteneur)
        self.text_edit.textChanged.connect(self.marquer_modifie)
        self.modifie = False

    def habillage_bouton(self, bouton):
        bouton.setStyleSheet("""
            QPushButton {
                color: #4e3728;
                border: 1px solid #ffaa43;
                border-radius: 8px;
                padding: 6px 16px;
                margin: 5px;
                background-color: white;
                font-weight: normal;
            }
            QPushButton:hover {
                background-color: #ffaa43;
                color: white;
            }
        """)

    def charger_tags(self):
        """placer les tags au démarrage dans l'éditeur"""
        if self.chemin_tags.exists():
            with open(self.chemin_tags, "r", encoding="utf-8") as f:
                self.text_edit.setPlainText(f.read())

    def quitter_sauvegarder(self):
        "enregister les changements"
        if self.modifie:
            with open(self.chemin_tags, "w", encoding="utf-8") as f:
                f.write(self.text_edit.toPlainText())
        self.close()

    def marquer_modifie(self):
        "le texte a été modié"
        self.modifie = True    

    def quitter_sans_enregistrer(self):
        "Quitter sans enregistrer"
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editeur = Editeur_tags()
    editeur.show()
    app.exec()


