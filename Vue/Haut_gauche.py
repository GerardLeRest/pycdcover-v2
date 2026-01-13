#!/usr/bin/env python3
"""
Haut_GAUCHE.py : gestion de la partie haute gauche de l'interface
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtCore import QObject, Signal, Slot
from pathlib import Path

class Haut_gauche(QObject):
    """affichage dans la fenêtre haut gauche"""

    album_selectionne = Signal(dict)

    def __init__(self):
        """initialisation"""
        super().__init__()
         # ex: [ "Radiohead - OK Computer", "Pink Floyd - Animals"]
        self.tableau: list[object] = [] # clé: ariste-aflbum de self.tableau
        # ex: {"Radiohead - OK Computer": {...},"Pink Floyd - Animals": {...}}
        self.albums: dict[str, dict] = {}
        self.fichier_tags_principal: Path = Path.home() / "PyCDCover" / "tags.txt"
        self.fichier_tags_secours: Path = (
            Path(__file__).resolve().parent.parent / "ressources" / "PyCDCover" / "tags2.txt"
        )

    def charger_depuis_fichier(self) -> dict:
        """Charge tous les albums et remplit self.albums + self.tableau."""
        self.tableau.clear()
        self.albums.clear()
        fichier = self.choisir_fichier_tags()
        if fichier is None:
            return {}
        lignes = self.lire_lignes(fichier)
        self.parser_fichier(lignes)
        self.nettoyer_photos_non_utilisees()
        return self.albums
    
    def nettoyer_photos_non_utilisees(self) -> None:
        """Supprime les photos dans thumbnails/ qui ne sont plus dans le dictionnaire self.albums."""
        thumbnails = Path.home() / "PyCDCover" / "thumbnails"
        if not thumbnails.exists():
            return
        # Images encore utilisées d'après tags.txt
        images_valides = { album["couverture"] for album in self.albums.values() }
        # Parcours du dossier thumbnails
        for fichier in thumbnails.iterdir():
            if fichier.is_file() and fichier.name not in images_valides:
                try:
                    fichier.unlink()
                    print(f"[SUPPRIMÉ] {fichier.name}")
                except Exception as e:
                    print(f"[ERREUR] Impossible de supprimer {fichier.name} : {e}")

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

    def parser_fichier(self, lignes: list[str]) -> None:
        """Analyse toutes les lignes et construit les albums."""
        artiste = album = annee = genre = couverture = None
        chansons = []
        for ligne in lignes:
            if ligne.startswith("C:"):
                artiste = ligne[2:].strip()
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
        left, right = ligne.split(" - ", 1)
        left, right = left.strip(), right.strip()
        if left.isdigit() and len(left) == 4:
            try:
                annee = int(left)
            except ValueError:
                annee = None
            genre = right or None
        else:
            try:
                num = int(left)
                chansons.append({"numero": num, "titre": right})
            except ValueError:
                annee = None
                genre = right or None
        return artiste, album, annee, genre, chansons

    def finaliser_album(self, artiste, album, annee, genre, couverture, chansons) -> None:
        """Ajoute un album complet dans les structures de données."""
        if not artiste or not album:
            return
        if not couverture:
            couverture = f"{artiste} - {album}.jpg"
        cle = f"{artiste} - {album}"
        self.tableau.append(cle)
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

