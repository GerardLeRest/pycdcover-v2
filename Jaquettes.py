#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyCDCover – Téléchargement automatique des jaquettes d’albums
à partir du fichier tags.txt (extrait du CD).
Crée les images dans ~/PyCDCover/thumbnails.
Version finale – Gérard Le Rest, 2025
"""

import os
import io
import re
import sys
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtCore import Qt, QTimer


# --------------------------------------------------------
# Lecture du fichier tags.txt
# --------------------------------------------------------
def lire_tags(fichier="tags.txt"):
    """Lit le fichier tags.txt et renvoie [(artiste, album), ...]."""
    albums = []
    artiste, album = None, None
    if not os.path.exists(fichier):
        print("❌ Fichier tags.txt introuvable.")
        return albums

    with open(fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne.startswith("C:"):
                artiste = ligne[2:].strip()
            elif ligne.startswith("A:"):
                album = ligne[2:].strip()
            elif ligne == "" and artiste and album:
                albums.append((artiste, album))
                artiste, album = None, None
        if artiste and album:
            albums.append((artiste, album))
    return albums


# --------------------------------------------------------
# Nettoyage des noms pour la recherche MusicBrainz
# --------------------------------------------------------
def nettoyer_nom(nom):
    """Supprime parenthèses, crochets et mots inutiles."""
    # Supprimer tout contenu entre (), [], {}
    nom = re.sub(r"[\(\[\{].*?[\)\]\}]", "", nom)

    # Supprimer les mots parasites
    nom = re.sub(
        r"\b(remaster(ed)?|disc|cd|deluxe|version|edition|bonus|anniversary|remix|mono|stereo)\b",
        "",
        nom,
        flags=re.IGNORECASE
    )

    # Supprimer tirets et espaces multiples
    nom = re.sub(r"[-_]+", " ", nom)
    nom = re.sub(r"\s{2,}", " ", nom)

    return nom.strip()


# --------------------------------------------------------
# Classe Jaquette
# --------------------------------------------------------
class Jaquette:
    """Télécharge ou crée une jaquette à partir de MusicBrainz."""

    def __init__(self, artiste, album, dossier):
        self.artiste = nettoyer_nom(artiste)
        self.album = nettoyer_nom(album)
        self.dossier = Path(dossier).expanduser()
        self.dossier.mkdir(parents=True, exist_ok=True)
        self.chemin = self.dossier / f"{self.artiste} - {self.album}.jpg"
        self.user_agent = "PyCDCover/1.0 (Gérard Le Rest)"

    # --- Recherche ---------------------------------------------------------
    def _recherche_musicbrainz(self):
        q = f'releasegroup:"{self.album}" AND artist:"{self.artiste}"'
        url = f"https://musicbrainz.org/ws/2/release-group/?query={q}&fmt=json&limit=1"
        try:
            r = requests.get(url, headers={"User-Agent": self.user_agent}, timeout=10)
            data = r.json()
            groupes = data.get("release-groups", [])
            return groupes[0]["id"] if groupes else None
        except Exception:
            return None

    # --- Téléchargement ----------------------------------------------------
    def _telecharger_image(self, id_release):
        if not id_release:
            return None
        url = f"https://coverartarchive.org/release-group/{id_release}/front"
        try:
            r = requests.get(url, headers={"User-Agent": self.user_agent}, timeout=10)
            if r.status_code == 200:
                return r.content
        except Exception:
            return None
        return None

    # --- Image de secours --------------------------------------------------
    def _image_secours(self):
        """Crée une image orange avec texte centré."""
        taille = 512
        img = Image.new("RGB", (taille, taille), (255, 140, 0))
        draw = ImageDraw.Draw(img)
        texte = f"{self.artiste}\n{self.album}"
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
        except Exception:
            font = ImageFont.load_default()
        tw, th = draw.multiline_textbbox((0, 0), texte, font=font)[2:]
        draw.multiline_text(((taille - tw) / 2, (taille - th) / 2),
                            texte, fill=(255, 255, 255),
                            font=font, align="center")
        return img

    # --- Public ------------------------------------------------------------
    def creer(self, forcer=False):
        """Crée la jaquette et retourne le chemin."""
        if self.chemin.exists() and not forcer:
            print(f"✔ Déjà présent : {self.chemin.name}")
            return self.chemin

        id_release = self._recherche_musicbrainz()
        donnees = self._telecharger_image(id_release)
        if donnees:
            try:
                image = Image.open(io.BytesIO(donnees)).convert("RGB")
                image.thumbnail((512, 512))
                image.save(self.chemin, "JPEG", quality=90)
                print(f"✓ Jaquette enregistrée : {self.chemin.name}")
                return self.chemin
            except Exception:
                pass

        # Si échec → image orange de secours
        image = self._image_secours()
        image.save(self.chemin, "JPEG", quality=90)
        print(f"⚠ Jaquette de secours créée : {self.chemin.name}")
        return self.chemin


# --------------------------------------------------------
# Interface PySide6 avec QProgressBar
# --------------------------------------------------------
class TelechargementUI(QWidget):
    """Fenêtre avec barre de progression pour les jaquettes."""

    def __init__(self, albums):
        super().__init__()
        self.albums = albums
        self.total = len(albums)
        self.compteur = 0

        self.setWindowTitle("Téléchargement des jaquettes")
        self.setFixedSize(400, 120)

        layout = QVBoxLayout()
        self.label = QLabel("Préparation…")
        self.label.setAlignment(Qt.AlignCenter)
        self.progress = QProgressBar()
        self.progress.setRange(0, self.total)
        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        self.setLayout(layout)

        QTimer.singleShot(500, self.lancer_telechargement)

    def lancer_telechargement(self):
        dossier_thumbs = Path("~/PyCDCover/thumbnails").expanduser()

        for artiste, album in self.albums:
            self.compteur += 1
            self.label.setText(f"[{self.compteur}/{self.total}] {artiste} – {album}")
            QApplication.processEvents()

            j = Jaquette(artiste, album, dossier_thumbs)
            j.creer()

            self.progress.setValue(self.compteur)
            QApplication.processEvents()

        self.label.setText("✅ Terminé !")
        QTimer.singleShot(1500, self.close)


# --------------------------------------------------------
# Programme principal
# --------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    albums = lire_tags("tags.txt")

    if not albums:
        print("Aucun album trouvé dans tags.txt.")
        sys.exit(0)

    fen = TelechargementUI(albums)
    fen.show()
    sys.exit(app.exec())
