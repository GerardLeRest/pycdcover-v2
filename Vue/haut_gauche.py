#!/usr/bin/env python3
"""
Haut_GAUCHE.py : gestion de la partie haute gauche de l'interface
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtCore import QObject, Signal, Slot
from pathlib import Path

class HautGauche(QObject):
    """affichage dans la fenêtre haut gauche"""

    album_selectionne = Signal(dict)

    def __init__(self):
        """initialisation"""
        super().__init__()
         # ex: [ "Radiohead - OK Computer", "Pink Floyd - Animals"]
        self.liste_artistes_albums: list[str] = [] 
        # Exemple : {'The Codebreakers - Best of PyCDCover': {'artiste': 'The Codebreakers',
        # 'album': 'Best of PyCDCover', 'annee': 2023, 'genre': 'Rock',
        # 'couverture': 'The Codebreakers - Best of PyCDCover.jpg', 
        # 'chansons': [{'numero': 1, 'titre': 'Tonight Again'}, {'numero': 2, 'titre': 'Start Over'} ...
        self.albums: dict[str, dict] = {}
        self.fichier_tags_principal: Path = Path.home() / "PyCDCover" / "tags.txt"
        self.fichier_tags_secours: Path = (
            Path(__file__).resolve().parent.parent / "ressources" / "PyCDCover" / "tags2.txt"
        )

    def charger_depuis_fichier(self) -> dict:
        """Charge tous les albums et remplit self.albums + self.tableau."""
        self.liste_artistes_albums.clear()
        self.albums.clear()
        fichier = self.choisir_fichier_tags()
        if fichier is None:
            return {}
        lignes = self.lire_lignes(fichier)
        self.traiter_fichier(lignes)
        return self.albums
    
    def choisir_fichier_tags(self) -> Path | None:
        """Choisir le fichier tags.txt (principal ou secours)."""
        if self.fichier_tags_principal.exists():
            return self.fichier_tags_principal
        if self.fichier_tags_secours.exists():
            return self.fichier_tags_secours
        return None

    def lire_lignes(self, fichier: Path) -> list[str]:
        """Lit et retourne toutes les lignes du fichier."""
        with open(fichier, encoding="utf-8") as f:
            return [l.strip() for l in f.readlines()] + [""]

    def traiter_fichier(self, lignes: list[str]) -> None:
        """Analyse toutes les lignes et construit les albums."""
        artiste = album = annee = genre = couverture = None
        chansons = []
        for ligne in lignes:
            if ligne.startswith("C:"):
                artiste = ligne[2:].strip()
            elif ligne.startswith("A:"):
                album = ligne[2:].strip()
            elif " - " in ligne:
                artiste, album, annee, genre, chansons = self.traiter_ligne_avec_tiret(
                    ligne, artiste, album, annee, genre, chansons
                )
            elif ligne == "":
                self.finaliser_album(artiste, album, annee, genre, couverture, chansons)
                artiste = album = annee = genre = couverture = None
                chansons = []

    def traiter_ligne_avec_tiret(
        self, ligne: str, artiste, album, annee, genre, chansons
    ):
        """Traite une ligne contenant ' - ' (année/genre ou chanson)."""
        gauche, droite = ligne.split(" - ", 1) # séparation au niveau du tiret
        gauche, droite = gauche.strip(), droite.strip()
        if gauche.isdigit() and len(gauche) == 4:
            try:
                annee = int(gauche)
            except ValueError:
                annee = None
            genre = droite or None
        else:
            try:
                num = int(gauche)
                chansons.append({"numero": num, "titre": droite})
            except ValueError:
                annee = None
                genre = droite or None
        return artiste, album, annee, genre, chansons

    def finaliser_album(self, artiste, album, annee, genre, couverture, chansons) -> None:
        """Ajoute un album complet dans les structures de données."""
        if not artiste or not album:
            return
        if not couverture:
            couverture = f"{artiste} - {album}.jpg"
        cle = f"{artiste} - {album}"
        self.liste_artistes_albums.append(cle)
        self.albums[cle] = {
            "artiste": artiste,
            "album": album,
            "annee": annee,
            "genre": genre,
            "couverture": couverture,
            "chansons": chansons,
        }

    @Slot(str)
    def selectionner_album(self, cle: str) -> None:
        """Émet le signal avec les infos de l’album sélectionné."""
        infos_album = self.albums.get(cle)
        if infos_album:
            self.album_selectionne.emit(infos_album)