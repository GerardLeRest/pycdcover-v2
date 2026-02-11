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
from builtins import _

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
        self.table.setHorizontalHeaderLabels([_("Titre"),_("Piste"),_("Album"),_("Artiste"), _("Année")])
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
                padding: 6px;
            }
            QTableWidget {
                color: #7C7C7C;   /* ✔️ gris léger */
            }
            QTableView {
                color: #7C7C7C;   /* ✔️ pour forcer le viewport */
            }
        """)


        # mise en page
        en_tete = self.table.horizontalHeader() 
        en_tete.setDefaultSectionSize(32)  # fixe la hauteur des barre entière
        # police
        font = QFont("", 18, QFont.Bold)   # police par défaut, taille 18, en gras
        en_tete.setFont(font)
        en_tete.setStyleSheet("""
            QHeaderView::section {
                color: #6c6c6c;
                font-size: 16px;
                margin: 0px;
                padding: 4px;
            }
        """)
        en_tete.setSectionResizeMode(QHeaderView.Interactive)
        en_tete.setStretchLastSection(False)
        # Titre
        en_tete.setSectionResizeMode(0, QHeaderView.Stretch)
        # Piste
        en_tete.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # Album
        en_tete.setSectionResizeMode(2, QHeaderView.Stretch)
        # Artiste
        en_tete.setSectionResizeMode(3, QHeaderView.Stretch)
        # Année
        en_tete.setSectionResizeMode(4, QHeaderView.ResizeToContents)

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

