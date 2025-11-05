from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from typing import Any

class Haut_droit(QWidget):
    ROW_H = 36        # hauteur uniforme des valeurs
    GAP   = 40        # espace entre blocs
    TOP   = 70       # marge haute pour descendre le premier bloc

    def __init__(self, nom_artiste: str, album: str, annee: str, genre: str):
        super().__init__()
        # chaines de caractère
        self.nom_artiste = nom_artiste
        self.album = album
        self.annee = annee
        self.genre = genre  

        self.tableau=[] # mémorise les labels (uniquement les valeurs, pas les titres)

        # construire l'UI
        self.assembler_elements()

    def label_titre(self, texte: str) -> QLabel:
        """placer le titre"""
        lab = QLabel(texte, self)
        lab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        lab.setFont(QFont("", 18, QFont.Bold)) # "": police par défaut du système
        lab.setStyleSheet("color: #ffaa43; margin:0; padding:0;")
        lab.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        return lab

    def label_valeur(self, texte: str) -> QLabel:
        """placer le contenu correspondant au titre"""
        lab = QLabel(texte, self)
        lab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        lab.setFixedHeight(self.ROW_H) 
        lab.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        lab.setStyleSheet("""
            font-size: 16px;
            color: #4e3728;
            border: 0.5px solid #6b5e4f;
            padding-left: 5px;
            border-radius: 8px;
        """)
        # on mémorise ce label pour pouvoir le mettre à jour
        self.tableau.append(lab)
        return lab

    def bloc(self, titre: str, valeur: str) -> QWidget:
        """création du bloc"""
        w = QWidget(self)   # bloc vide
        vbox = QVBoxLayout(w) # dans ce bloc, les élémnets seront empilés verticalment
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(10)   # espace entre le titre et la valeur
        vbox.addWidget(self.label_titre(titre))
        vbox.addWidget(self.label_valeur(valeur))
        return w

    def assembler_elements(self) -> None:
        "assembler l'ensemble des éléments"
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(8, self.TOP, 8, 8)  # TOP applique le décalage
        layout_principal.setSpacing(self.GAP)
        
        # blocs simples
        layout_principal.addWidget(self.bloc("Artiste", self.nom_artiste))
        layout_principal.addWidget(self.bloc("Album", self.album))

        # bloc " Année - Genre"
        ligne = QWidget(self)
        hbox = QHBoxLayout(ligne)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(16)
        hbox.addWidget(self.bloc("Année", self.annee))
        hbox.addWidget(self.bloc("Genre", self.genre))
        layout_principal.addWidget(ligne)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    def MAJ_haut_droit(self, infos:dict[str, Any]) -> None:
        """Mise à jour les labels"""
        # ordre des labels dans self.tableau :
        # [0] = artiste, [1] = album, [2] = annee, [3] = genre
        print(self.tableau)
        if len(self.tableau) >= 4:
            self.tableau[0].setText(infos.get('artiste', ""))
            self.tableau[1].setText(infos.get('album', ""))
            self.tableau[2].setText(str(infos.get('annee') or ""))
            self.tableau[3].setText(infos.get('genre', ""))