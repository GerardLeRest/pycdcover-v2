#!/usr/bin/env python3
"""
Fen_Titre.py: fenêtre de saisie du titre
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QApplication, QPushButton,
    QHBoxLayout, QLineEdit, QDialog,QMessageBox )
import sys
from PySide6.QtCore import Signal
from Vue.utils import centrer_fenetre # fonction


class Fen_Titre(QDialog):
    """fenetre de saisie du nom"""

    titre_selectionne = Signal(str)

    def __init__(self):
        super().__init__()
        self.titre: str | None = None # titre du cd
        self.champ: QLineEdit | None = None # champ de la fenètre
        self.initialiser()

    def initialiser(self)->None:
        """construction de la fenêtre"""
        self.setWindowTitle("Titre du CD")            
        layoutV = QVBoxLayout()
        layoutV.setContentsMargins(20, 20, 20, 20)

        # label
        label = QLabel ("Saisir le titre du CD", self)
        label.setStyleSheet("font-size: 15px; padding: 14px 0;")
        layoutV.addWidget(label)
        
        # layout Horizontal
        layoutH =QHBoxLayout()
        # champ
        self.champ = QLineEdit()
        self.champ.setPlaceholderText("Titre du CD")
        self.champ.setStyleSheet("""
                border: 1px solid #6b5e4f;
                border-radius: 8px;
                padding: 6px 16px;
                margin-right: 20px
                             """)
        layoutH.addWidget(self.champ)
        # bouton
        bouton = QPushButton("Ok", self)
        bouton.setStyleSheet("""
            QPushButton {
                color: #4e3728;
                border: 1px solid #6b5e4f;
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
        bouton.clicked.connect(self.emission_titre)
        layoutH.addWidget(bouton)
        layoutV.addLayout(layoutH)

        self.setLayout(layoutV)
        
    def showEvent(self, event) -> None:
        """Centrage automatique à l'affichage du dialogue."""
        super().showEvent(event)
        centrer_fenetre(self) # voir Vue/utils.py
        self.champ.setFocus() # positionement du curseur dans le champ


    def emission_titre (self) -> None:
        """vérifie la validité du champ"""
        if not self.champ.text():
            QMessageBox.warning(self, "Erreur", "Le champ est vide.")
            return
        elif len(self.champ.text())>50:
            QMessageBox.warning(self, "Erreur", "Le titre est trop long (> 40 car).")
            return
        else:
            # on doit émettre avant la fermeture de la fenetre
            self.titre_selectionne.emit(self.champ.text())
            self.accept()

    def recup_titre(self) ->str:
        """Renvoie le titre saisi"""
        return self.titre

if __name__ == "__main__":
    application = QApplication(sys.argv)
    dialog = Fen_Titre() # dialog: convention Qt pour une fenetre
    if dialog.exec():  # fenêtre modale
        print("Titre saisi :", dialog.recup_titre())  # OK : maintenant ça retourne une str
    else:
        print("Annulé.")
    # on peut quitter proprement (évite de bloquer sur application.exec())
    sys.exit(0)