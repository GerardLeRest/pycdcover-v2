#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Haut_milieu.py — Affiche le nom de l’artiste, le nom de l’album
et la jaquette correspondante (modifiable par l’utilisateur).
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                               QFileDialog, QMessageBox)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from pathlib import Path
from typing import Any


class Haut_milieu(QWidget):
    """Zone supérieure centrale : affiche artiste, album et image de jaquette."""

    def __init__(self, nom_artiste: str, nom_album: str, chemin_photo_artiste: str):
        """Initialise la zone avec artiste, album et image."""
        super().__init__()

        self.nom_artiste = nom_artiste
        self.nom_album = nom_album
        self.chemin_photo_artiste = chemin_photo_artiste

        self.label_artiste = QLabel()
        self.label_album = QLabel()
        self.label_image = QLabel()

        self.dossier_pycdcover = Path.home() / "PyCDCover"

    def assembler_elements(self) -> None:
        """Assemble les labels et le bouton dans un layout vertical."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Label ARTISTE
        self.label_artiste = QLabel(self.nom_artiste, self)
        self.label_artiste.setAlignment(Qt.AlignCenter)
        self.label_artiste.setStyleSheet("""
            font-size: 28px;
            color: #4e3728;
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


    def charger_photo(self, infos_album) -> None:
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
            print(f"Couverture chargée : {chemin}")
        else:
            print(f"Couverture introuvable : {chemin}")
            self.label_image.clear()
            self.pixmap_actuelle = None

    def MAJ_haut_milieu(self, infos: dict[str, Any]) -> None:
        """Met à jour les labels artiste et album, et recharge la jaquette."""
        self.infos_album = infos  # 🔸 On garde le dictionnaire pour le bouton
        self.label_artiste.setText(infos.get('artiste') or "")
        self.label_album.setText(infos.get('album') or "")
        couverture = infos.get("couverture", "")
        self.charger_photo(couverture)
        print("Chargement de :", couverture)