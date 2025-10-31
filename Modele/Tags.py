#!/usr/bin/env python3
"""
Tags.py — Récupère les tags MP3 d’un CD et les enregistre dans ~/PyCDCover/tags.txt
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QProgressBar, QLabel, QFileDialog, QMessageBox
)
from PySide6.QtCore import Signal
from pathlib import Path
from mutagen import File as MutaFile
import sys


class Tags(QMainWindow):

    tags_termines = Signal() # signal

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Extraction des tags MP3")
        self.resize(300, 100)
        # interface
        layout = QVBoxLayout()
        self.label = QLabel("Prêt à extraire les tags.")
        self.progress = QProgressBar() # barre de progression
        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        layout.setContentsMargins(20, 10, 20, 20)  # gauche, haut, droite, bas
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def recuperer_tags(self):
        """Sélectionne un dossier et détecte les albums simples ou multiples (CD1, CD2...), puis extrait les tags."""
        chemin = QFileDialog.getExistingDirectory(self, "Choisir le répertoire du CD", "/media")
        if not chemin:
            return

        lecteur = Path(chemin)
        albums = []

        for d in lecteur.iterdir():
            if not d.is_dir():
                continue
            sous_dossiers = [sd for sd in d.iterdir() if sd.is_dir()]
            if sous_dossiers:
                albums.extend(sous_dossiers)  # CD1, CD2, etc.
            else:
                albums.append(d)

        if not albums:
            albums = [lecteur]

        total = sum(len(list(a.glob("*.mp3"))) for a in albums)
        if total == 0:
            QMessageBox.information(self, "Aucun MP3", "Aucune piste MP3 trouvée.")
            return

        self.progress.setRange(0, total)
        self.label.setText("Extraction en cours...")
        QApplication.processEvents()

        # 👇 Ici on appelle directement la suite
        self.fichier_sortie(albums)


        
    def fichier_sortie(self, albums):
        # Fichier de sortie
        fichier = Path.home() / "PyCDCover" / "tags.txt"
        fichier.parent.mkdir(exist_ok=True)
        count = 0
        with open(fichier, "w", encoding="utf-8") as f:
            for album in albums:
                mp3s = self._mp3s_tries_par_piste(album)
                if not mp3s: # fichier .jpeg, etc...
                    continue
                # information du de l'album
                info0 = MutaFile(mp3s[0], easy=True)
                artiste = info0.get("artist", ["Inconnu"])[0]
                nom_album = info0.get("album", ["Inconnu"])[0]
                genre = info0.get("genre", ["Inconnu"])[0]
                annee = self._annee(info0)
                f.write(f"C: {artiste}\nA: {nom_album}\n{annee} - {genre}\n")
                # Numérotation des titres
                for i, mp3 in enumerate(mp3s, 1):
                    titre = MutaFile(mp3, easy=True).get("title", [mp3.stem])[0]
                    f.write(f"{i} - {titre}\n")
                    count += 1
                    self.progress.setValue(count)
                    QApplication.processEvents()
                f.write("\n")
        QMessageBox.information(self, "Terminé", "Extraction terminée avec succès !")
        self.tags_termines.emit() # emission signal

    def _mp3s_tries_par_piste(self, dossier: Path):
        """Retourne la liste des fichiers MP3 triés par numéro de piste."""
        fichiers = []
        for mp3 in dossier.glob("*.mp3"):
            try:
                num = int(MutaFile(mp3, easy=True).get("tracknumber", ["0"])[0].split("/")[0])
            except Exception:
                num = 0
            fichiers.append((num, mp3))
        return [m for _, m in sorted(fichiers, key=lambda x: x[0])]

    def _annee(self, info):
        """Extrait l’année à partir des tags si possible."""
        for cle in ("originaldate", "date", "year"):
            if cle in info:
                val = info[cle][0][:4] # retient 2025 dans "2025/10/23" 
                if val.isdigit():  #123 => ok - 1g7 => fauc 
                    return val
        return "Inconnue"

if __name__ == "__main__":
    application = QApplication(sys.argv)
    tags = Tags()
    tags.show()
    albums = tags.recuperer_tags()
    tags.fichier_sortie(albums)
    # on réfère sys.exit(app.exec()) à app.exec()
    sys.exit(application.exec()) # adapté à windows (sorte 0:ok 1:nok -plus propre)