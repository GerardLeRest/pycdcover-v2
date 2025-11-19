#!/usr/bin/env python3
"""
Image_devant — Module de récupération et normalisation des images d’albums

Ce module a été entièrement conçu et structuré par ChatGPT (GPT-5, 2025).
Je (Gérard Le Rest) l’utilise comme un composant externe, 
au même titre qu’une bibliothèque tierce.

Je n’en revendique pas la paternité intellectuelle.
Je n’ai pas vocation à en expliquer les détails internes.
Je l’emploie “en boîte noire”, sans garantie de débogage.

Toute la logique complexe de recherche iTunes / MusicBrainz,
du cache JSON et du traitement des jaquettes relève de l’IA.

Petite fenêtre de progression affichée pendant la récupération des images.
Émet le signal 'telechargement_termine' quand le processus est fini.
"""

from __future__ import annotations
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Signal, Qt, QThread, QObject
from pathlib import Path
from Modele.recup_images_avant import Image_devant
import re
from typing import Any


# ========================================================================
# --- Thread worker ------------------------------------------------------
# ========================================================================

class WorkerTelechargement(QObject):
    """
    Télécharge les jaquettes (ou les crée) dans un thread séparé.
    Émet deux signaux :
      - progression(index, total)
      - telechargement_termine()
    """
    telechargement_termine: Signal = Signal()
    progression: Signal = Signal(int, int)

    def __init__(self, albums: list[dict[str, Any]]) -> None:
        super().__init__()
        self.albums: list[dict[str, Any]] = albums

    def run(self) -> None:
        """Boucle principale de téléchargement."""
        dossier_thumbnails: Path = Path.home() / "PyCDCover" / "thumbnails"
        dossier_thumbnails.mkdir(parents=True, exist_ok=True)

        total: int = len(self.albums)
        precedent: str | None = None  # pour éviter les doublons (ex : The Wall (I)/(II))

        for i, album in enumerate(self.albums, start=1):
            try:
                artiste: str = album["artiste"]
                titre: str = album["album"]

                # Supprime les parenthèses (I)/(II) pour comparer
                base_titre: str = re.sub(r"\s*\(.*?\)", "", titre).strip()

                # Si c’est le même album que le précédent → on saute
                if base_titre == precedent:
                    print(f"↩ Jaquette déjà créée pour : {base_titre}")
                    self.progression.emit(i, total)
                    continue

                # Crée ou télécharge la jaquette
                image = Image_devant(artiste, titre)
                image.creer()

                precedent = base_titre
                self.progression.emit(i, total)

            except Exception as e:
                print(f"⚠ Erreur sur l'album {album}: {e}")
                self.progression.emit(i, total)
                continue

        # Tous les téléchargements terminés
        self.telechargement_termine.emit()
        print("Téléchargement terminé pour tous les albums.")


# ========================================================================
# --- Interface utilisateur ----------------------------------------------
# ========================================================================

class TelechargementUI(QWidget):
    """Fenêtre de suivi du téléchargement des images."""
    telechargement_termine: Signal = Signal()

    def __init__(self, albums: list[dict[str, Any]]) -> None:
        super().__init__()
        self.setWindowTitle("Téléchargement des images")
        self.resize(340, 120)

        layout = QVBoxLayout(self)
        self.label = QLabel("Téléchargement des pochettes...")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.progress = QProgressBar()
        self.progress.setRange(0, len(albums))
        layout.addWidget(self.progress)

        # Thread de travail
        self.worker = WorkerTelechargement(albums)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        # Connexions
        self.worker.progression.connect(self._mettre_a_jour_progression)
        self.worker.telechargement_termine.connect(self._telechargement_fini)
        self.thread.started.connect(self.worker.run)

        self.thread.start()

    def _mettre_a_jour_progression(self, index: int, total: int) -> None:
        """Met à jour la barre de progression et le texte."""
        self.progress.setValue(index)
        self.label.setText(f"Téléchargement {index}/{total}")

    def _telechargement_fini(self) -> None:
        """Méthode appelée quand tous les téléchargements sont terminés."""
        self.label.setText("Téléchargement terminé")
        self.telechargement_termine.emit()
        self.thread.quit()
        self.thread.wait()