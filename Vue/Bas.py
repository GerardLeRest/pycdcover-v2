from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QApplication,
    QTableWidget, QTableWidgetItem, QHeaderView
)
import sys
from typing import Any
from PySide6.QtGui import QFont


class Bas(QWidget):
    
    def __init__(self, chansons: list, album: str, artiste: str, annee: int):
        """initialisation"""
        super().__init__()
        self.chansons = chansons
        self.album = album
        self.artiste = artiste
        self.annee = str(annee)  # toujours stockée comme chaîne
        self.initialiser()

    def initialiser(self) -> None:
        """initialisation de la classe"""
        layout = QVBoxLayout()

        # Création du tableau
        self.table = QTableWidget(len(self.chansons), 5)
        self.table.setHorizontalHeaderLabels(["Titre", "Piste", "Album", "Artiste", "Année"])
        self.table.verticalHeader().setVisible(False)

        # Remplissage
        self.remplir_table()

        # taille et couleur du texte
        self.table.setStyleSheet("""
            QTableWidget::item {
            font-size: 16px;
            color: #4e3728;
            padding: 6px
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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    chansons = [
        {"numero": 1, "titre": "Tunnel of Love"},
        {"numero": 2, "titre": "Romeo and Juliet"},
        {"numero": 3, "titre": "Skateaway"},
        {"numero": 4, "titre": "Expresso Love"},
        {"numero": 5, "titre": "Hand in Hand"}
    ]

    bas = Bas(chansons, "Making Movies", "Dire Straits", 1980)
    bas.resize(850, 300)
    bas.show() 
    sys.exit(app.exec())

