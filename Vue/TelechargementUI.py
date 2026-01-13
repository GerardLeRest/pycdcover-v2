#!/usr/bin/env python3

"""
# PyCDCover - Récupération des images
# Cette fenêtre gère la création des miniatures (thumbnails) utilisées
# pour composer les jaquettes.
"""

from __future__ import annotations
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QTimer, Signal
from Modele.recup_images_avant import ImageDevant
from typing import Any
from builtins import _

class TelechargementUI(QWidget):

    telechargement_termine = Signal()

    def __init__(self, albums: list[dict[str, Any]]) -> None:
        super().__init__()
        self.albums = albums
        self.index = 0
        self.total = len(albums)
        # fenêtre de barre de progression
        self.setWindowTitle(_("Téléchargement des images"))
        self.resize(340, 120)
        layout = QVBoxLayout(self)
        self.label = QLabel(_("Téléchargement en cours..."))
        self.label.setAlignment(Qt.AlignCenter)
        # barre de progression
        self.progress = QProgressBar()
        self.progress.setRange(0, self.total)
        # attachement au layout
        layout.addWidget(self.label)
        layout.addWidget(self.progress)

        QTimer.singleShot(0, self._suivant)

    # ------------------------------------------------------------------
    def _suivant(self) -> None:
        """Crée la miniature de l’album courant puis passe au suivant."""
        if self.index >= self.total:
            self.label.setText(_("Téléchargement terminé"))
            self.telechargement_termine.emit()
            QTimer.singleShot(500, self.close)
            return
        album = self.albums[self.index]
        artiste = album.get("artiste", "")
        titre = album.get("album", "")
        ImageDevant(artiste, titre).creer()
        self.index += 1
        self.progress.setValue(self.index)
        self.label.setText(
            _("Téléchargement {}/{}").format(self.index, self.total)
        )
        QTimer.singleShot(0, self._suivant)
