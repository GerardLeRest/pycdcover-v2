#!/usr/bin/env python3

"""
Récupère une image (miniature) à partir du nom de l'artiste
et du titre de l'album.
"""

import io
import os
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from typing import Optional
from urllib.parse import quote

BASE_DIR = Path(__file__).resolve().parent

# -----------------------------------------------------------
# Lecture des tags
# -----------------------------------------------------------

def lire_tags(fichier: str = "tags.txt") -> list[dict[str, str]]:
    """
    Lit le fichier tags.txt et renvoie une liste d'albums :
    [
        {
            "artiste": "Nom de l'artiste",
            "album": "Titre de l'album"
        },
        ...
    ]
    """
    albums: list[dict[str, str]] = []
    artiste: str | None = None

    if not os.path.exists(fichier):
        return albums

    with open(fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne.startswith("C:"):
                artiste = ligne[2:].strip()
            elif ligne.startswith("A:") and artiste:
                albums.append({
                    "artiste": artiste,
                    "album": ligne[2:].strip()
                })

    return albums

def get_itunes_cover(artiste: str, album: str) -> Optional[str]:
    """Retourne l'URL de la jaquette iTunes ou None."""
    try:
        term = quote(f"{artiste} {album}")
        url = f"https://itunes.apple.com/search?term={term}&entity=album&limit=1"
        data = requests.get(url, timeout=5).json()

        if data.get("resultCount", 0) > 0: # nombre de résultats trouvés
            # url de la pochette du premier album (100x100 px)
            url = data["results"][0]["artworkUrl100"]
            return url.replace("100x100bb", "600x600bb") # agrandissement
        return None
    except Exception:
        return None

# -----------------------------------------------------------
# Image de couverture
# -----------------------------------------------------------

class ImageDevant:
    def __init__(self, artiste: str, album: str) -> None:
        self.artiste = artiste
        self.album = album
        self.chemin = (
            Path.home()
            / "PyCDCover"
            / "thumbnails"
            / f"{artiste} - {album}.jpg"
        )
        self.chemin.parent.mkdir(parents=True, exist_ok=True)

    def creer(self) -> Path:
        url = get_itunes_cover(self.artiste, self.album)
        if url:
            data = requests.get(url).content
            img = Image.open(io.BytesIO(data))
        else:
            img = self._image_secours()

        img = self._image_carre(img)
        img.save(self.chemin, "JPEG", quality=90)
        return self.chemin

    def _image_carre(self, img: Image.Image, size: int = 512) -> Image.Image:
        img = img.convert("RGB")
        img.thumbnail((size, size))
        fond = Image.new("RGB", (size, size), (255, 140, 0))
        fond.paste(
            img,
            ((size - img.width) // 2, (size - img.height) // 2)
        )
        return fond

    def _image_secours(self) -> Image.Image:
        font = ImageFont.truetype(
            BASE_DIR / "ressources" / "polices" / "FreeSerif.ttf",
            32
        )
        img = Image.new("RGB", (512, 512), (255, 140, 0))
        draw = ImageDraw.Draw(img)
        draw.text(
            (20, 216),
            f"{self.artiste}\n{self.album}",
            fill="white",
            font=font
        )
        return img
