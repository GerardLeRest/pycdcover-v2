# ========================================================================
# PyCDCover - Classe : RecupImagesAvant
# Auteur principal : GPT-5
# Supervision, direction et résolution des incohérences : Gérard Le Rest
# ========================================================================

"""
    Petite fenêtre de progression affichée pendant la récupération des images.
    Émet le signal 'telechargement_termine' quand le processus est fini.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Signal, Qt, QThread, QObject
from pathlib import Path
from Modele.recup_images_avant import Image_devant
import re


class WorkerTelechargement(QObject):
    """
    Télécharge les jaquettes (ou les crée) dans un thread séparé.
    Émet deux signaux :
      - progression(index, total)
      - telechargement_termine()
    """
    telechargement_termine = Signal()
    progression = Signal(int, int)

    def __init__(self, albums):
        super().__init__()
        self.albums = albums

    def run(self):
        """Boucle principale de téléchargement."""
        dossier_thumbnails = Path.home() / "PyCDCover" / "thumbnails"
        dossier_thumbnails.mkdir(parents=True, exist_ok=True)

        total = len(self.albums)
        precedent = None  # 🔸 pour éviter les doublons (ex : The Wall (I)/(II))

        for i, album in enumerate(self.albums, start=1):
            try:
                artiste = album["artiste"]
                titre = album["album"]

                # 🔹 Supprime les parenthèses (I)/(II) pour comparer
                base_titre = re.sub(r"\s*\(.*?\)", "", titre).strip()

                # 🔸 Si c’est le même album que le précédent → on saute
                if base_titre == precedent:
                    print(f"↩ Jaquette déjà créée pour : {base_titre}")
                    self.progression.emit(i, total)
                    continue

                # 🔹 Crée ou télécharge la jaquette
                image = Image_devant(artiste, titre)
                image.creer()

                precedent = base_titre
                self.progression.emit(i, total)

            except Exception as e:
                print(f"⚠ Erreur sur l'album {album}: {e}")
                self.progression.emit(i, total)
                continue

        # 🔔 Tous les téléchargements terminés
        self.telechargement_termine.emit()
        print("✅ Téléchargement terminé pour tous les albums.")



class TelechargementUI(QWidget):
    telechargement_termine = Signal()

    def __init__(self, albums: list):
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

        # --- Thread de travail ---
        self.worker = WorkerTelechargement(albums)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        self.worker.progression.connect(self._mettre_a_jour_progression)
        self.worker.telechargement_termine.connect(self._telechargement_fini)
        self.thread.started.connect(self.worker.run)

        self.thread.start()

    def _mettre_a_jour_progression(self, index, total):
        self.progress.setValue(index)
        self.label.setText(f"Téléchargement {index}/{total}")

    def _telechargement_fini(self):
        self.label.setText("Téléchargement terminé ✅")
        self.telechargement_termine.emit()
        self.thread.quit()
        self.thread.wait()
