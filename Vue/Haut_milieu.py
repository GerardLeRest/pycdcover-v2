#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Haut_milieu.py — Affiche le nom de l’artiste, le nom de l’album
et la jaquette correspondante (modifiable par l’utilisateur).
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QFileDialog)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal, Slot
from pathlib import Path
from typing import Any
from builtins import _



class Haut_milieu(QWidget):
    """Zone supérieure centrale : affiche artiste, album et image de jaquette."""

        
    demande_image_changee = Signal(str) # quand l'image est affichée (demande d'enregistrement)

    def __init__(self, nom_artiste: str, nom_album: str, chemin_photo_artiste: Path):
        """Initialise la zone avec artiste, album et image."""
        super().__init__()
        # Données affichées
        self.nom_artiste: str = nom_artiste
        self.nom_album: str = nom_album
        self.chemin_photo_artiste: Path = chemin_photo_artiste
        # Labels des informations
        self.label_artiste: QLabel | None = None
        self.label_album: QLabel | None = None
        self.label_image: QLabel | None = None
        # Chemins
        self.dossier_pycdcover: Path = Path.home() / "PyCDCover"
        self.dossier_thumbnails: Path | None = None
        # État interne
        self.pixmap_actuelle: QPixmap | None = None
        self.infos_album: dict[str, Any] | None = None

    def assembler_elements(self) -> None:
        """Assemble les labels et le bouton dans un layout vertical."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        # Label ARTISTE
        self.label_artiste = QLabel(self.nom_artiste, self)
        self.label_artiste.setAlignment(Qt.AlignCenter)
        self.label_artiste.setStyleSheet("""
            font-size: 32px;
            color: #2E2E2E;
            font-weight: 600;
        """)
        layout.addWidget(self.label_artiste, alignment=Qt.AlignHCenter)
        # Label ALBUM
        self.label_album = QLabel(self.nom_album, self)
        self.label_album.setAlignment(Qt.AlignCenter)
        self.label_album.setStyleSheet("""
            font-size: 18px;
            color: #6b5e4f;
        """)
        layout.addWidget(self.label_album, alignment=Qt.AlignHCenter)
        # Zone d’image
        self.label_image = QLabel(self)
        self.label_image.setFixedSize(200, 200)
        self.label_image.setAlignment(Qt.AlignCenter)
        self.label_image.setStyleSheet("""
            QLabel {
                background: #ffffff;
                border: 1px solid #e0d6c6;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.label_image, alignment=Qt.AlignHCenter)
        # Bouton "Changer"
        # self.bouton_changer = QPushButton("Changer", self)
        # self.bouton_changer.setFixedSize(140, 40)
        # self.bouton_changer.setStyleSheet("""
        #     QPushButton {
        #         color: #4e3728;
        #         border: 1px solid #6b5e4f;
        #         border-radius: 8px;
        #         padding: 6px 16px;
        #         background-color: white;
        #         font-weight: normal;
        #     }
        #     QPushButton:hover {
        #         background-color: #ffaa43;
        #         color: white;
        #     }
        # """)
        # layout.addWidget(self.bouton_changer, alignment=Qt.AlignHCenter)
        # self.bouton_changer.clicked.connect(self.action_changer)


    def charger_photo(self, infos_album: dict[str, Any]) -> None:
        """Charge la jaquette depuis le nom ou le dictionnaire fourni."""
        couverture = infos_album if isinstance(infos_album, str) else infos_album.get("couverture")
        self.dossier_thumbnails = self.dossier_pycdcover / "thumbnails"
        if not any(self.dossier_thumbnails.iterdir()):
            self.dossier_thumbnails = Path(__file__).resolve().parent.parent / "ressources" / "PyCDCover" / "thumbnails"
        chemin = self.dossier_thumbnails / couverture
        if chemin.exists():
            pixmap = QPixmap(str(chemin)).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label_image.setPixmap(pixmap)
            self.pixmap_actuelle = pixmap
        else:
            self.label_image.clear()
            self.pixmap_actuelle = None

    # @Slot()
    # def action_changer(self) -> None:
    #     """Permet de choisir une nouvelle image via une boîte de dialogue."""
    #     fichier, _ = QFileDialog.getOpenFileName(
    #         self,
    #         "Choisir une nouvelle jaquette",
    #         "",
    #         "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
    #     )
    #     if not fichier:
    #         return
    #     # Charger et afficher l'image
    #     self.couverture = Path(fichier).name
    #     pixmap = QPixmap(fichier).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    #     self.label_image.setPixmap(pixmap)
    #     self.pixmap_actuelle = pixmap   # empêche sa suppression
    #     # Notifier le contrôleur
    #     self.demande_image_changee.emit(self.couverture)

    def MAJ_haut_milieu(self, infos: dict[str, Any]) -> None:
        """Met à jour les labels artiste et album, et recharge la jaquette."""
        self.infos_album = infos  # 🔸 On garde le dictionnaire pour le bouton
        self.label_artiste.setText(infos.get('artiste') or "")
        self.label_album.setText(infos.get('album') or "")
        couverture = infos.get("couverture", "")
        self.charger_photo(couverture)