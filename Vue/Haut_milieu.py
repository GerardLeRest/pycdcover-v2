# haut_milieu.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os
from typing import Any


class Haut_milieu(QWidget):

    def __init__(self, nom_artiste:str, nom_album:str, chemin_photo_artiste:str):
        """intialisation"""
        super().__init__()
        self.nom_artiste = nom_artiste
        self.nom_album = nom_album
        self.chemin_photo_artiste = chemin_photo_artiste
        self.label_album=QLabel()
        self.label_artiste=QLabel()
        self.label_image=QLabel()

        self.assembler_elements()

    def assembler_elements(self)->None:
        """assembler les différents widgets"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)   # marges extérieures (g, h, d, b)
        layout.setSpacing(20)                       # espace entre les widgets

        # Artiste 
        self.label_artiste = QLabel(self.nom_artiste, self)
        self.label_artiste.setAlignment(Qt.AlignCenter)# centrage horizontal + vertical du texte à l'intérieur du label
        self.label_artiste.setStyleSheet("font-size: 28px; color: #4e3728; font-weight: 600;")
        # ajout du widget et centrage Horizontale et centrage horizontal du label dans le layout
        layout.addWidget(self.label_artiste, alignment=Qt.AlignHCenter) 

        # Album 
        self.label_album = QLabel(self.nom_album, self)
        self.label_album.setAlignment(Qt.AlignCenter)
        self.label_album.setStyleSheet("font-size: 18px; color: #6b5e4f;")
        layout.addWidget(self.label_album, alignment=Qt.AlignHCenter)

        #Image
        self.label_image = QLabel(self)
        self.label_image.setFixedSize(200, 200)     # zone visuelle stable
        self.label_image.setAlignment(Qt.AlignCenter)
        self.label_image.setStyleSheet("""
            QLabel {
                background: #ffffff;
                border: 1px solid #e0d6c6;   /* bordure valide */
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.label_image, alignment=Qt.AlignHCenter)

        # Charger la première image
        self.charger_photo(self.chemin_photo_artiste)

        # Bouton
        self.bouton_changer = QPushButton("Changer", self)
        self.bouton_changer.setFixedSize(140, 40)  # plus épais + largeur stable
        self.bouton_changer.setStyleSheet("""
            QPushButton {
                color: #4e3728;
                border: 2px solid #ffaa43;
                border-radius: 8px;
                padding: 6px 16px;
                background-color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ffaa43;
                color: white;
            }
        """)
        self.bouton_changer.clicked.connect(self.changer_image)
        layout.addWidget(self.bouton_changer, alignment=Qt.AlignHCenter)

    def charger_photo(self, chemin: str) -> None:
        """Charge l'image en s'adaptant à la zone 200x200 (en gardant le ratio)."""
        if not chemin:
            self.label_image.clear()
            return
        pm = QPixmap(chemin).scaled(
            200, 200,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.label_image.setPixmap(pm)
        self.chemin_photo_artiste = chemin

    def changer_image(self)->None:
        """changer l'image"""
        fichier, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir une photo",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if fichier:
            self.charger_photo(fichier)

    def MAJ_haut_milieu(self, infos:dict[str, Any]) -> None:
        """Mise à jour les labels"""
        self.label_artiste.setText(infos.get('artiste') or "")
        self.label_album.setText(infos.get('album') or "")
        os.chdir("/home/gerard/PyCDCover/thumbnails/") # LIGNE A SUPPRIMER PLUS TARD
        couverture = infos.get('couverture') or ""
        self.charger_photo(couverture)