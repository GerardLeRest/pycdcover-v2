#!/usr/bin/env python3

"""
Tags.py — Récupère les tags MP3 d’un CD et les enregistre dans ~/PyCDCover/tags.txt
Auteur : Gérard Le Rest (2025)
"""
from pathlib import Path
from mutagen import File as MutaFile
from PySide6.QtCore import QObject, Signal


class Tags(QObject):
    
    """Récupérer tous les tags MP3 (artiste, album, année, genre, titres, numéros de piste)
    puis les enregistrer proprement dans ~/PyCDCover/tags.txt,
    avec une barre de progression et des messages d’information (classe Progress_tags)."""

    progress = Signal(int)
    termine = Signal()

    def __init__(self):
        super().__init__()
        self.fichier_tags = Path.home() / "PyCDCover" / "tags.txt" # fichier des tags
        self.nbre_albums = 0 # nbre albums

    def _lister_albums(self, lecteur: Path) -> list[Path]:
        albums = []
        for d in lecteur.iterdir():
            if not d.is_dir():
                continue
            # cas des doubles albums qui deviennent des albums distincts
            sous_dossiers = [sd for sd in d.iterdir() if sd.is_dir()]
            if sous_dossiers:
                albums.extend(sous_dossiers)
            else:
                albums.append(d)
        # retourne [lecteur] si albums est vide -[]
        return albums or [lecteur]

    def extraire_tags(self, chemin: Path) -> None:
        """extraction des tags depuis le dossier chemin"""
        # chemin non vide ou mauvais chemin 
        if not chemin or not chemin.exists():
            return
        albums = self._lister_albums(chemin)
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
                f.write(f"C: {artiste} \n")
                nom_album = info0.get("album", ["Inconnu"])[0]
                chemin = nom_album
                album = Path(chemin).name
                f.write(f"A: {album} \n")
                genre = info0.get("genre", ["Inconnu"])[0]
                annee = self._annee(info0)
                f.write(f"{annee} - {genre} \n")
                # comprage des albums
                self.nbre_albums = i + 1
                # traitement des textes des chansons
                for j, mp3 in enumerate(mp3s, 1):
                    titre = MutaFile(mp3, easy=True).get("title", [mp3.stem])[0]
                    ligne = f"{j} - {titre}"
                    f.write(f"{ligne} \n")
                    count += 1
                    #########################
                    self.progress.emit(count) #  le modèle doit signaler qu’il a avancé

                   
                f.write("\n")
        # couper les lignes rop longues
        self.couper_texte(self.nbre_albums)
        ################################################
        self.termine.emit() # le modèle dit qu'il a fini
        

    def couper_texte(self, nbre_albums: int) -> None:
        """couper ici pour être plus rapide:
        1. extraction e tenregistrement des méta-données - recuperer_tags
        2. couper les lignes trop longues et pas aumiliue d'un mot""" 
        # récupération des lignes du fichier tags.txt
        lignes = []
        # lecture du fichier
        with open(self.fichier_tags, "r", encoding="utf-8") as f:
            lignes = [ligne.rstrip("\n") for ligne in f.readlines()]
        # coupe des lignes trop longues et les écrit
        with open(self.fichier_tags, "w", encoding="utf-8") as f:
            for ligne in lignes:
                if nbre_albums < 8:
                    pos = ligne.rfind(" ", 0, 30) # 30: espace avant le 30ème caractère
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
                num = int(MutaFile(mp3, easy=True).get("tracknumber", ["0"])[0].split("/")[0])
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

#""""""""""""""""""""""""""""""""""""""""""""""""
# Tests
#"""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == "__main__":
    tags = Tags()
    tags.extraire_tags(Path("/tmp/mp3_test"))
