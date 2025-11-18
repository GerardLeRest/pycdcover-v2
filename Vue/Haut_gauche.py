#!/usr/bin/env python3
"""
Haut_GAUCHE.py: gestion de la partie haute gauche de l'interface
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtCore import QObject, Signal, Slot
from pathlib import Path
from Modele.recup_images_avant import nettoyer_nom

class Haut_gauche(QObject):
    """affichage dans la fentre haut gauche"""
    
    album_selectionne = Signal(dict)
    def __init__(self):
        super().__init__()
        self.tableau = []
        self.albums = {}
        self.fichier_tags_principal = Path.home() / "PyCDCover" / "tags.txt" # fichier du dosssier personnel
        # fichier de l'album de démonstration
        self.fichier_tags_secours = Path(__file__).resolve().parent.parent / "ressources" / "PyCDCover" / "tags2.txt"

    def charger_depuis_fichier(self) -> dict:
        """Charge les albums depuis le premier fichier de tags disponible."""
        self.tableau.clear()
        self.albums.clear()
        albums = {}

        # Sélection du fichier existant
        if self.fichier_tags_principal.exists():
            print(f"Fichier trouvé : {self.fichier_tags_principal}")
            self.fichier_tags = self.fichier_tags_principal
        elif self.fichier_tags_secours.exists():
            print(f"Fichier trouvé : {self.fichier_tags_secours}")
            self.fichier_tags = self.fichier_tags_secours
        else:
            print("Aucun fichier tags.txt trouvé.")
            return {}

        # Lecture du fichier choisi
        with open(self.fichier_tags, encoding="utf-8") as f:
            lignes = [l.strip() for l in f.readlines()]

        artiste = album = None
        annee = genre = couverture = None
        chansons = []

        # Analyse ligne par ligne du fichier
        for ligne in lignes + [""]:  # la ligne vide force l'enregistrement du dernier album
            if ligne.startswith("C:"):
                artiste = ligne[2:].strip()
            elif ligne.startswith("A:"):
                album = ligne[2:].strip()
                album = f"{nettoyer_nom(album)}"
            elif ligne.lower().endswith((".jpg", ".jpeg", ".png")):
                couverture = ligne.strip()
                couverture = f"{nettoyer_nom(couverture)}"
            elif " - " in ligne:
                left, right = ligne.split(" - ", 1)
                left, right = left.strip(), right.strip()

                # Ligne de type "1987 - Rock" ou "01 - Song Title"
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
            elif ligne == "":
                # Fin d'un bloc album : on enregistre les données collectées
                if artiste and album:
                    cle = f"{artiste} - {album}"

                    # Si aucune couverture trouvée, on la déduit automatiquement
                    if not couverture:
                        couverture = f"{artiste} - {album}.jpg"

                    self.tableau.append(cle)
                    albums[cle] = {
                        "artiste": artiste,
                        "album": album,
                        "annee": annee,
                        "genre": genre,
                        "couverture": couverture,
                        "chansons": chansons,
                    }

                # Réinitialisation pour l'album suivant
                artiste = album = annee = genre = couverture = None
                chansons = []

        self.albums = albums
        return albums

    def afficher(self) -> None:
        """Affiche dans la console la liste des albums chargés (pour debug)."""
        for cle, infos in self.albums.items():
            print(cle, "=>", infos["annee"], infos["genre"])
            for t in infos["chansons"]:
                print("   ", t["numero"], "-", t["titre"])
            print(infos["couverture"])

    @Slot(str)
    def selectionner_album(self, cle: str) -> None:
        """Émet le signal avec les infos de l’album sélectionné."""
        infos_album = self.albums.get(cle)
        if infos_album:
            self.album_selectionne.emit(infos_album)