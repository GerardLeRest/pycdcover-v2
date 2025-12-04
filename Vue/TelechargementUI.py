#!/usr/bin/env python3

"""
# PyCDCover - Récupération des images
# Cette fenêtre gère la création des miniatures (thumbnails) utilisées
# pour composer les jaquettes. Les albums sont traités un par un sans
# thread, grâce à QTimer, afin de garder une interface fluide et fiable
# sur tous les systèmes.
Je ne cherche pas à en comprendre les détails internes. 
"""

from __future__ import annotations
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QTimer, Signal
from pathlib import Path
from Modele.recup_images_avant import Image_devant
import re
from typing import Any


class TelechargementUI(QWidget):
    telechargement_termine: Signal = Signal()

    def __init__(self, albums: list[dict[str, Any]]) -> None:
        super().__init__()

        self.albums = albums
        self.index = 0
        self.total = len(albums)
        self.traites: set[str] = set()

        self.dossier = Path.home() / "PyCDCover" / "thumbnails"
        self.dossier.mkdir(parents=True, exist_ok=True)

        # --- UI -----------------------------------------------------------
        self.setWindowTitle("Téléchargement des images")
        self.resize(340, 120)

        layout = QVBoxLayout(self)
        self.label = QLabel("Initialisation...")
        self.label.setAlignment(Qt.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setRange(0, self.total)

        layout.addWidget(self.label)
        layout.addWidget(self.progress)

        # Démarre immédiatement le traitement
        QTimer.singleShot(0, self._traiter_suivant)

    # --------------------------------------------------------------------
    def _normaliser(self, titre: str) -> str:
        titre = re.sub(r"\s*\(.*?\)", "", titre)
        titre = re.sub(r"disc\s*\d+", "", titre, flags=re.IGNORECASE)
        return titre.strip().lower()

    # --------------------------------------------------------------------
    def _thumbnail_existe(self, artiste: str, titre: str) -> bool:
        nom = f"{artiste}-{titre}".replace("/", "_").replace(" ", "_").lower()
        return (self.dossier / f"{nom}.jpeg").exists()

    # --------------------------------------------------------------------
    def _traiter_suivant(self) -> None:
        """Traite UN album, puis demande à Qt d'appeler la suite."""
        if self.index >= self.total:
            self.label.setText("Téléchargement terminé")
            self.telechargement_termine.emit()
            QTimer.singleShot(600, self.close)
            return

        album = self.albums[self.index]
        artiste = album.get("artiste", "")
        titre = album.get("album", "")

        titre_norm = self._normaliser(titre)

        try:
            # doublons
            if titre_norm not in self.traites:

                # miniature déjà existante ?
                if not self._thumbnail_existe(artiste, titre):
                    Image_devant(artiste, titre).creer()

                self.traites.add(titre_norm)

        except Exception:
            # on ignore, comme avant
            pass

        # UI update
        self.index += 1
        self.progress.setValue(self.index)
        self.label.setText(f"Téléchargement {self.index}/{self.total}")

        # Continue sans bloquer
        QTimer.singleShot(0, self._traiter_suivant)
