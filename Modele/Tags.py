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
import sys, unicodedata
from builtins import _

class Tags(QMainWindow):
    """Récupérer tous les tags MP3 (artiste, album, année, genre, titres, numéros de piste)
    puis les enregistrer proprement dans ~/PyCDCover/tags.txt,
    avec une barre de progression et des messages d’information."""

    tags_termines = Signal() # signal

    def __init__(self):
        super().__init__()
        self.setWindowTitle(_("Extraction des tags MP3..."))
        self.resize(300, 100)
        # interface
        layout = QVBoxLayout()
        self.label = QLabel(_("Prêt à extraire les tags"))
        self.fichier_tags = Path.home() / "PyCDCover" / "tags.txt" # fichier des tags
        self.progress: QProgressBar | None = None
        self.nbre_albums = 0 # nbre albums
        layout.addWidget(self.label)
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        layout.setContentsMargins(20, 10, 20, 20)  # gauche, haut, droite, bas
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        

    def recuperer_tags(self)->None:
        """Créer la lsites des albums (dictionnaires) * artistes et albums - liste d'objets Path"""
        # fenetre du choix du dossier des albums
        chemin = QFileDialog.getExistingDirectory(self, _("Choisir le répertoire des chansons"), _("/media"))
        if not chemin:
            return
        lecteur = Path(chemin)
        albums = [] # liste des dossiers des albums
        #parcours des dosiers d'albums
        for d in lecteur.iterdir():
            if not d.is_dir():
                continue
            sous_dossiers = [sd for sd in d.iterdir() if sd.is_dir()]
            if sous_dossiers:
                albums.extend(sous_dossiers)  # CD1, CD2, etc.
            else:
                albums.append(d)
        # cas des maquettes -on force le lecteur comme unique album
        if not albums:
            albums = [lecteur]
        total = sum(len(list(a.glob("*.mp3"))) for a in albums)
        if total == 0:
            QMessageBox.information(self, _("Aucun MP3"), _("Aucune piste MP3 trouvée."))
            return
        # barre de progressions
        self.progress.setRange(0, total)
        self.label.setText(_("Extraction en cours..."))
        QApplication.processEvents()
        # Ici on appelle directement la suite
        self.fichier_sortie(albums)
        
    def fichier_sortie(self, albums: list) -> None:
        """écrire le fichier tags.txt"""
        count = 0
        self.nbre_albums = 0
        with open(self.fichier_tags, "w", encoding="utf-8") as f:
            for i, album in enumerate (albums):
                mp3s = self._mp3s_tries_par_piste(album)
                if not mp3s:
                    continue
                # récupération des méta-données
                info0 = MutaFile(mp3s[0], easy=True)
                artiste = info0.get("artist", ["Inconnu"])[0]
                # nettoyage avant écriture en utf8
                artiste = self.clean(artiste)
                f.write(f"C: {artiste} \n")
                nom_album = info0.get("album", ["Inconnu"])[0]
                nom_album = self.clean(nom_album)
                chemin = nom_album
                album = Path(chemin).name
                f.write(f"A: {album} \n")
                genre = info0.get("genre", ["Inconnu"])[0]
                genre = self.clean(genre)
                annee = self._annee(info0)
                f.write(f"{annee} - {genre} \n")
                # comprage des albums
                self.nbre_albums = i + 1
                # traitement des textes des chansons
                for j, mp3 in enumerate(mp3s, 1):
                    titre = MutaFile(mp3, easy=True).get("title", [mp3.stem])[0]
                    ligne = f"{j} - {titre}"
                    ligne = self.clean(ligne)
                    f.write(f"{ligne} \n")
                    count += 1
                    self.progress.setValue(count)
                    QApplication.processEvents()
                f.write("\n")
        # couper les lignes rop longues
        self.couper_texte(self.nbre_albums)
        # indiquent que les tags ont écrits        
        self.tags_termines.emit()
        # Barre de progression
        self.progress.setValue(self.progress.maximum())  # sécurité : barre à 100 %
        QApplication.processEvents()                      # rafraîchissement immédiat
        self.close()                                      # FERMETURE AUTOMATIQUE

    def clean(self, s: str) -> str:
        """nettoyage pou utf-8"""
        # normalisation unicode
        s = unicodedata.normalize("NFC", s)
        # suppression des caractères de contrôle
        return "".join(c for c in s if c.isprintable())
            
    
    def couper_texte(self, nbre_albums: int) -> int:
        """couper ici pour être plus rapide:
        1. extraction e tenregistrement des méta-données - recuperer_tags
        2. couper les lignes trop longues et pas aumiliue d'un mot""" 
        # récupération des lignes du fichier tags.txt
        lignes = []
        with open(self.fichier_tags, "r", encoding="utf-8") as f:
            lignes = [ligne.rstrip("\n") for ligne in f.readlines()]
        # coupe des lignes trop longues
        with open(self.fichier_tags, "w", encoding="utf-8") as f:
            for ligne in lignes:
                if nbre_albums < 8:
                    pos = ligne.rfind(" ", 0, 30) # 30: espace avant le 40ème caractère
                else:
                    pos = ligne.rfind(" ", 0, 40)
                if pos == -1:
                    # pas d'espace → on n'essaye même pas de couper
                    f.write(ligne + "\n")
                else:
                    # on coupe au dernier espace avant 30 ou 40 caractères    
                    f.write(ligne[:pos] + "\n")
        
    def _mp3s_tries_par_piste(self, dossier: Path) -> list[Path]:
        """Retourne la liste des fichiers MP3 triés par numéro de piste."""
        fichiers = []
        for mp3 in dossier.glob("*.mp3"):
            try:
                num = int(MutaFile(mp3, easy=list).get("tracknumber", ["0"])[0].split("/")[0])
            except Exception:
                num = 0
            fichiers.append((num, mp3))
        return [m for _, m in sorted(fichiers, key=lambda x: x[0])]

    
    def _annee(self, info: dict[str, list[str]]) -> str:
        """Extrait l’année à partir des tags si possible."""
        for cle in ("originaldate", "date", "year"):
            if cle in info:
                val = info[cle][0][:4]  # retient 2025 dans "2025/10/23"
                if val.isdigit():       # 123 => ok - 1g7 => faux 
                    return val
        return "Inconnue"

# ------------------------------------------------------------------------------
# Programme principal de test
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tags = Tags()
    tags.show()
    tags.recuperer_tags()   # ← on redemande le dossier
    sys.exit(app.exec())