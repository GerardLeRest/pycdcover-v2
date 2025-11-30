#!/usr/bin/env python3

"""
Editeur.py: Editer/modifier les tags dans une fenêtre
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtWidgets import (
    QWidget, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QWidget, QApplication
)
from PySide6.QtCore import Qt, Signal
from pathlib import Path
from Vue.utils import centrer_fenetre
import sys


class Editeur_tags(QWidget):
    """Editer/modifier les tags dans une fenêtre"""

    # signal pour mettre à a jour les données albums et tableau (Haut_gauche)
    tags_enregistres = Signal() 

    def __init__(self, parent=None):
        super().__init__(parent)
        #pour pouvoir mettre à jours les donnée d'autres méthodes - voir + bas
        self.parent = parent   # référence vers la fenêtre principale
        self.setWindowTitle("Éditeur de tags")
        self.resize(300, 400)
        # fichier tags
        self.chemin_tags: Path = Path.home() / "PyCDCover" / "tags.txt"
        self.text_edit: QTextEdit | None = None
        self.modifie: bool = False
        # dessiner l'interface
        self.interface()

    def interface(self) -> None:
        """Interaction entre les boutons et l'éditeur"""
        layout = QVBoxLayout()
        # zone de texte
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)
        # charger le texte au démarrage
        self.charger_tags()
        # layout horizontal pour les boutons
        layout_hor = QHBoxLayout()
        # bouton valider
        valider = QPushButton("Valider", self)
        valider.setFixedWidth(100)
        self.habillage_bouton(valider)
        layout_hor.addWidget(valider)
        valider.clicked.connect(self.quitter_sauvegarder)
        # bouton quitter
        abandonner = QPushButton("Quitter", self)
        abandonner.setFixedWidth(100)
        self.habillage_bouton(abandonner)
        layout_hor.addWidget(abandonner, alignment=Qt.AlignRight)
        abandonner.clicked.connect(self.quitter_sans_enregistrer)
        # ajout du layout horizontal
        layout.addLayout(layout_hor)
        # appliquer le layout au QDialog
        conteneur = QWidget()
        conteneur.setLayout(layout)
        self.setLayout(layout)
        # détection des modifications
        self.text_edit.textChanged.connect(self.marquer_modifie)
        self.modifie = False
        centrer_fenetre(self)

    def habillage_bouton(self, bouton: QPushButton) -> None:
        bouton.setStyleSheet("""
            QPushButton {
                color: #4e3728;
                border: 1px solid #6b5e4f;
                border-radius: 8px;
                padding: 6px 10px;
                margin: 10px;
                background-color: white;
                font-weight: normal;
            }
            QPushButton:hover {
                background-color: #ffaa43;
                color: white;
            }
        """)

    def charger_tags(self) -> None:
        """Placer les tags au démarrage dans l'éditeur"""
        if self.chemin_tags.exists():
            with open(self.chemin_tags, "r", encoding="utf-8") as f:
                self.text_edit.setPlainText(f.read())

    def quitter_sauvegarder(self) -> None:
        """Enregistrer les changements et prévenir la fenêtre principale."""
        if self.modifie:
            with open(self.chemin_tags, "w", encoding="utf-8") as f:
                f.write(self.text_edit.toPlainText())

            # prévenir la fenêtre principale que les tags ont été modifiés
            self.tags_enregistres.emit()
        self.close()

    def marquer_modifie(self) -> None:
        """Signal que le texte a été modifié"""
        self.modifie = True

    def quitter_sans_enregistrer(self) -> None:
        """Quitter sans enregistrer"""
        # prévenir la fenêtre principale que les tags ont été modifiés
        self.close()


    


# Programme principal de test
if __name__ == "__main__":
    app = QApplication(sys.argv)
    editeur = Editeur_tags()
    editeur.show()
    app.exec()
