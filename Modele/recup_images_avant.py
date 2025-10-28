#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image_devant – Gère la lecture des tags et la création
ou récupération des jaquettes musicales.
Projet PyCDCover – ChatGPT, 2025
"""

import os
import io
import re
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QApplication
from PySide6.QtCore import Qt, QTimer, Signal



# -----------------------------------------------------------
# --- Fonctions utilitaires ---------------------------------
# -----------------------------------------------------------
def lire_tags(fichier="tags.txt"):
    """Lit le fichier tags.txt et renvoie une liste [(artiste, album), ...]."""
    albums = []
    artiste, album = None, None
    if not os.path.exists(fichier):
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


def nettoyer_nom(nom):
    """Nettoie les noms d’artistes ou d’albums."""
    if not nom:
        return ""
    nom = re.sub(r"[\(\[\{].*?[\)\]\}]", "", nom)
    nom = re.sub(
        r"\b(remaster(ed)?|disc|cd|deluxe|version|edition|bonus|anniversary|remix|mono|stereo)\b",
        "",
        nom,
        flags=re.IGNORECASE,
    )
    nom = re.sub(r"[-_]+", " ", nom)
    nom = re.sub(r"\s{2,}", " ", nom)
    return nom.strip()


# -----------------------------------------------------------
# --- Classe principale -------------------------------------
# -----------------------------------------------------------
class Image_devant:
    """Télécharge ou crée une jaquette à partir de MusicBrainz."""

    def __init__(self, artiste, album, dossier):
        """Initialisation"""
        telechargement_termine = Signal()
        # dossier
        dossier_utilisateur = Path.home()
        self.dossier_pycovercd = dossier_utilisateur / "PyCDCover"
        self.dossier_thumbnails = self.dossier_pycovercd / "thumbnails"
        # nettoyage des titres 
        self.artiste = nettoyer_nom(artiste)
        self.album = nettoyer_nom(album)
        self.chemin = self.dossier_thumbnails / f"{self.artiste} - {self.album}.jpg"
        #User-Agent pour MusicBrainz
        self.user_agent = "PyCDCover/1.0 (Gérard Le Rest)"


    def _recherche_musicbrainz(self):
        """Recherche d'abord avec artiste+album, puis album seul si échec."""
        def requete(query):
            url = f"https://musicbrainz.org/ws/2/release-group/?query={query}&fmt=json&limit=1"
            try:
                r = requests.get(url, headers={"User-Agent": self.user_agent}, timeout=10)
                data = r.json()
                groupes = data.get("release-groups", [])
                return groupes[0]["id"] if groupes else None
            except Exception:
                return None

        # --- 1️ tentative stricte
        q1 = f'releasegroup:"{self.album}" AND artist:"{self.artiste}"'
        id_release = requete(q1)

        # --- 2️ si rien trouvé, on tente plus large
        if not id_release:
            q2 = f'releasegroup:"{self.album}"'
            id_release = requete(q2)
            if id_release:
                print(f"⚠ Trouvé avec recherche simplifiée pour : {self.artiste} – {self.album}")

        return id_release


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

    def _image_secours(self):
        """Crée une image orange avec le nom de l’album."""
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

    def creer(self, forcer=False):
        """Crée ou télécharge la jaquette et retourne le chemin."""
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
                print(f"✓ Image enregistrée : {self.chemin.name}")
                return self.chemin
            except Exception:
                pass

        image = self._image_secours()
        image.save(self.chemin, "JPEG", quality=90)
        print(f"⚠ Jaquette de secours créée : {self.chemin.name}")
        return self.chemin


# -----------------------------------------------------------
# --- Classe de progression ---------------------------------
# -----------------------------------------------------------
class TelechargementUI(QWidget):
    """Fenêtre de progression du téléchargement des jaquettes."""
    telechargement_termine = Signal()  # Déclaration du signal

    def __init__(self, albums, dossier):
        super().__init__()
        self.albums = albums
        self.dossier = dossier
        self.total = len(albums)
        self.compteur = 0

        self.setWindowTitle("Téléchargement des jaquettes")
        self.setFixedSize(400, 120)

        layout = QVBoxLayout()
        self.label = QLabel("Préparation…", alignment=Qt.AlignCenter)
        self.progress = QProgressBar()
        self.progress.setRange(0, self.total)
        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        self.setLayout(layout)

        QTimer.singleShot(500, self.lancer_telechargement)

    def lancer_telechargement(self):
        for artiste, album in self.albums:
            self.compteur += 1
            self.label.setText(f"[{self.compteur}/{self.total}] {artiste} – {album}")
            QApplication.processEvents()

            j = Image_devant(artiste, album, self.dossier)
            j.creer()

            self.progress.setValue(self.compteur)
            QApplication.processEvents()

        self.label.setText("Terminé !")
        QTimer.singleShot(1500, self.close)

        self.label.setText("Terminé !")
        self.telechargement_termine.emit()   # signal envoyé à la fenêtre principale
        QTimer.singleShot(1500, self.close)

