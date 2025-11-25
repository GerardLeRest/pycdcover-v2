# ========================================================================
# PyCDCover - Classe : RecupImagesAvant (version optimisée)
# Auteur principal : GPT-5 (optimisation)
# Supervision, direction et cohérence : Gérard Le Rest
# ========================================================================

from __future__ import annotations
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Signal, Qt, QThread, QObject
from pathlib import Path
from Modele.recup_images_avant import Image_devant
import re
from typing import Any


# ========================================================================
# --- Thread worker optimisé ---------------------------------------------
# ========================================================================

class WorkerTelechargement(QObject):
    """
    Thread de récupération des jaquettes.
    Améliorations :
      - Détection intelligente des doublons (dictionnaire)
      - Vérification de la jaquette déjà existante avant création
      - Robustesse en cas d'erreurs
      - Code plus lisible et plus compact
    """

    telechargement_termine: Signal = Signal()
    progression: Signal = Signal(int, int)

    def __init__(self, albums: list[dict[str, Any]]) -> None:
        super().__init__()
        self.albums = albums

        # Cache anti-doublons : évite de créer 2 fois la même jaquette
        self._albums_traités: set[str] = set()

        # Dossier thumbnails
        self.dossier_thumbnails = Path.home() / "PyCDCover" / "thumbnails"
        self.dossier_thumbnails.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------------------
    def _normaliser_titre(self, titre: str) -> str:
        """Supprime les annotations du type '(I)', 'Disc 2', etc."""
        titre = re.sub(r"\s*\(.*?\)", "", titre)
        titre = re.sub(r"disc\s*\d+", "", titre, flags=re.IGNORECASE)
        return titre.strip().lower()

    # --------------------------------------------------------------------
    def _thumbnail_existe(self, artiste: str, titre: str) -> bool:
        """Vérifie si une miniature existe déjà."""
        nom = f"{artiste}-{titre}".replace("/", "_").replace(" ", "_").lower()
        fichier = self.dossier_thumbnails / f"{nom}.jpeg"
        return fichier.exists()

    # --------------------------------------------------------------------
    def run(self) -> None:
        """Boucle principale du thread."""
        total = len(self.albums)

        for index, album in enumerate(self.albums, start=1):
            try:
                artiste = album["artiste"]
                titre = album["album"]

                titre_normalisé = self._normaliser_titre(titre)

                # Déjà traité ? → on skip
                if titre_normalisé in self._albums_traités:
                    print(f"↩ Déjà traité : {titre}")
                    self.progression.emit(index, total)
                    continue

                # Déjà présent sur disque ? → pas besoin de créer
                if self._thumbnail_existe(artiste, titre):
                    print(f"✓ Miniature déjà présente : {titre}")
                    self._albums_traités.add(titre_normalisé)
                    self.progression.emit(index, total)
                    continue

                # Création réelle de la miniature
                image = Image_devant(artiste, titre)
                image.creer()

                # Marqué comme traité
                self._albums_traités.add(titre_normalisé)
                self.progression.emit(index, total)

            except Exception as e:
                print(f"⚠ Erreur sur l'album {album}: {e}")
                self.progression.emit(index, total)
                continue

        # Fin du processus
        print("Téléchargement terminé pour tous les albums.")
        self.telechargement_termine.emit()



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

    # ------------------------------------------------------------------
    def _mettre_a_jour_progression(self, index: int, total: int) -> None:
        self.progress.setValue(index)
        self.label.setText(f"Téléchargement {index}/{total}")

    # ------------------------------------------------------------------
    def _telechargement_fini(self) -> None:
        self.label.setText("Téléchargement terminé")
        self.telechargement_termine.emit()
        self.thread.quit()
        self.thread.wait()