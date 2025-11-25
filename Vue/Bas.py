#!/usr/bin/env python3

"""
Bas.py - Affichage dans le tableau du logiviel
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QApplication,
    QTableWidget, QTableWidgetItem, QHeaderView
)
import sys
from typing import Any
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtCore import Qt

class Bas(QWidget):
    """affichage des méta-données du disque"""
    
    def __init__(self, chansons: list, album: str, artiste: str, annee: int):
        """initialisation"""
        super().__init__()
        self.chansons: list[dict[str, Any]] = chansons
        self.album: str = album
        self.artiste: str  = artiste
        self.annee: int = annee   
        self.table: QTableWidget | None =None
        self.initialiser()

    def initialiser(self) -> None:
        """initialisation de la classe"""
        layout = QVBoxLayout()

        # Création du tableau
        self.table = QTableWidget(len(self.chansons), 5)
        self.table.setHorizontalHeaderLabels(["Titre", "Piste", "Album", "Artiste", "Année"])
        self.table.verticalHeader().setVisible(False)
        # Empêche toute modification
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Empêche toute sélection de cellule
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setFocusPolicy(Qt.NoFocus) 
        # Remplissage
        self.remplir_table()

        # taille et couleur du texte
        self.table.setStyleSheet("""
            QTableWidget::item {
                font-size: 16px;
                color: #4e3728;
                padding: 6px;
            }
            QTableWidget::item:selected {
                background-color: #FF6633;
                color: white;
                font-weight: 600;
            }
        """)

        # mise en page
        header = self.table.horizontalHeader() 
        header.setDefaultSectionSize(32)  # fixe la hauteur des barre entière
        # police
        font = QFont("", 18, QFont.Bold)   # police par défaut, taille 18, en gras
        header.setFont(font)
        header.setStyleSheet("""
            QHeaderView::section {
                color: #ffaa43;
                font-size: 16px;
                margin: 0px;
                padding: 4px;
            }
        """)
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(False)
        # Titre
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        # Piste
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # Album
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        # Artiste
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        # Année
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        # lignes plus hautes (espace vertical)
        vh = self.table.verticalHeader()
        vh.setDefaultSectionSize(32)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def remplir_table(self) -> None:
        """Remplir le tableau avec les chansons actuelles."""
        for row, chanson in enumerate(self.chansons):
            titre = chanson.get("titre", "")
            numero = str(chanson.get("numero", ""))
            valeurs = [titre, numero, self.album, self.artiste, self.annee]

            for col, valeur in enumerate(valeurs):
                self.table.setItem(row, col, QTableWidgetItem(valeur))

    def MAJ_bas(self, infos: dict[str, Any]) -> None:
        """Mettre à jour le tableau avec un nouvel album."""
        if not isinstance(infos, dict):
            print("⚠️ infos reçues par MAJ_bas n'est pas un dict :", type(infos))
            return  # on sort proprement
        self.album = infos.get("album", "")
        self.artiste = infos.get("artiste", "")
        self.annee = str(infos.get("annee", ""))
        self.chansons = infos.get("chansons", [])
        self.table.setRowCount(len(self.chansons))
        self.remplir_table()


# ------------------------------------------------------------------------------
# Programme principal de test
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)

    chansons = [
        {"numero": 1,"titre": ""},
        {"numero": 2, "titre": ""},
        {"numero": 3, "titre": ""},
        {"numero": 4, "titre": ""},
        {"numero": 5, "titre": ""}
    ]
    bas = Bas(chansons, "", "", None)
    #bas = Bas(chansons, " ", " ", None)
    bas.resize(850, 300)
    bas.show() 
    sys.exit(app.exec())

