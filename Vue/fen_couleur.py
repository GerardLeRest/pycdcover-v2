#!/usr/bin/env python3
"""
Fen_Titre.py: fenêtre de saisie du titre
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtWidgets import (
    QLabel, QApplication, QPushButton, QRadioButton,
    QHBoxLayout, QVBoxLayout, QLineEdit, QDialog,QMessageBox, QGridLayout )
import sys
from PySide6.QtCore import Signal
# from Vue.centrer_fenetre import centrage_fenetre # fonction
import gettext 
_ = gettext.gettext

class FenCouleur(QDialog):
    """fenetre de saisie du nom"""

    couleur_selectionnee = Signal(str)

    def __init__(self):
        super().__init__()
        self.interface()
    
    def interface(self):
        """interface de la fenêtre"""
        layout = QVBoxLayout()
        # boutons radio
        layout.setContentsMargins(20, 20, 20, 20) # contour de 20
        self.radioBC = QRadioButton(_("Blanc cassé: ")) #F5F5F0
        self.radioGC = QRadioButton(_("Gris clair: ")) #D0D0D0
        self.radioBD = QRadioButton(_("Beige doux: ")) #E8DFC8
        layout.addWidget(self.radioBC)
        layout.addWidget(self.radioGC)
        layout.addWidget(self.radioBD)
        self.radioBC.setChecked(True)
        # bouton "valider"
        bouton = QPushButton(_("valider"))
        bouton.clicked.connect(self.recup_couleur)
        layout.addWidget(bouton)
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
        self.setLayout(layout)
        
    def recup_couleur(self):
        """récupération de la couleur chosie"""
        couleur_choisie = "" 
        if self.radioBC.isChecked():
           couleur_choisie= "#F5F5F0"
        elif self.radioGC.isChecked():
           couleur_choisie = "#D0D0D0"
        else:
            couleur_choisie = "#E8DFC8" 
        self.close()
        print (f"couleur_choisie: {couleur_choisie}")
        self.couleur_selectionnee.emit(couleur_choisie)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = FenCouleur()
    fenetre.exec()      # ⭐ important pour QDialog
    sys.exit(app.exec())