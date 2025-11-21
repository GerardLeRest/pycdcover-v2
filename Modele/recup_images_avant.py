#!/usr/bin/env python3
"""
Image_devant — Module de récupération et normalisation des images d’albums

Ce module a été entièrement conçu et structuré par ChatGPT (GPT-5, 2025).
Je (Gérard Le Rest) l’utilise comme un composant externe, 
alors je le considère comme une “boîte noire”.
"""

import os
import io
import re
import json
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote
from typing import Optional, Any, Iterable

from PIL import Image, ImageDraw, ImageFont

# -----------------------------------------------------------
# --- Fonctions utilitaires ---------------------------------
# -----------------------------------------------------------

def fusionner_artiste_album(artiste: str, album: str) -> tuple[str, str]:
    """
    Corrige les cas du type :
    "Alt-J - fsdfsd"
    "AC/DC - Back in Black"
    "Alt - J - Truc"

    Idée simple :
    - Si l'album est vide ET que l'artiste contient " - ",
      on suppose que la chaîne est "Artiste - Album" et on découpe.
    - Sinon on ne touche pas.
    """
    artiste = artiste.strip()
    album = album.strip()

    if " - " in artiste and not album:
        artiste_corr, album_corr = artiste.split(" - ", 1)
        return artiste_corr.strip(), album_corr.strip()

    return artiste, album


def get_itunes_cover(artiste: str, album: str) -> Optional[str]:
    """Recherche la jaquette sur iTunes et renvoie l'URL haute résolution."""
    try:
        recherche = quote(f"{artiste} {album}")
        url = f"https://itunes.apple.com/search?term={recherche}&entity=album&limit=1"
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            data = r.json()
            if data.get("resultCount", 0) > 0:
                image_url = data["results"][0]["artworkUrl100"]
                return image_url.replace("100x100bb", "600x600bb")
    except Exception as e:
        print(f"Erreur API iTunes pour {artiste} - {album} : {e}")
    return None


def lire_tags(fichier: str = "tags.txt") -> list[dict[str, Any]]:
    """
    Lit le fichier de tags et renvoie une liste de dict :
    {
        "artiste": str,
        "album": str,
        "couverture": str,
        "image_url": Optional[str]
    }
    """
    albums: list[dict[str, Any]] = []
    artiste: Optional[str] = None
    album: Optional[str] = None

    if not os.path.exists(fichier):
        return albums

    with open(fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne.startswith("C:"):
                artiste = ligne[2:].strip()
            elif ligne.startswith("A:"):
                album = ligne[2:].strip()
                if artiste and album:
                    couverture = f"{artiste} - {album}.jpg"
                    image_url = get_itunes_cover(artiste, album)
                    albums.append({
                        "artiste": artiste,
                        "album": album,
                        "couverture": couverture,
                        "image_url": image_url
                    })
    return albums


def nettoyer_nom(nom: str) -> str:
    """Nettoie les noms d’artistes ou d’albums sans casser les titres normaux."""
    if not nom:
        return ""

    # Suppression du texte entre parenthèses, crochets, accolades
    nom = re.sub(r"[\(\[\{].*?[\)\]\}]", "", nom)

    interdits = [
        "remaster", "remastered", "deluxe", "version", "edition",
        "bonus", "anniversary", "remix", "mono", "stereo",
        "disc", "cd"
    ]

    for mot in interdits:
        nom = re.sub(rf"(?i)\b{mot}\b", "", nom)

    # Espaces multiples -> un espace
    nom = re.sub(r"\s{2,}", " ", nom)
    return nom.strip()


# -----------------------------------------------------------
# --- Gestion du cache JSON ---------------------------------
# -----------------------------------------------------------
CACHE_PATH = Path.home() / "PyCDCover" / "cache.json"
_CACHE_MEMO: dict[str, str] = {}


def lire_cache() -> dict[str, str]:
    """
    Charge le cache MusicBrainz en mémoire une seule fois.
    Les appels suivants réutilisent le dict en mémoire.
    """
    global _CACHE_MEMO

    if _CACHE_MEMO:
        return _CACHE_MEMO

    if CACHE_PATH.exists():
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                _CACHE_MEMO = json.load(f)
        except Exception:
            _CACHE_MEMO = {}

    return _CACHE_MEMO


def ecrire_cache(cache: dict[str, str]) -> None:
    """
    Met à jour le cache en mémoire et sur disque.
    """
    global _CACHE_MEMO
    _CACHE_MEMO = cache

    try:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(_CACHE_MEMO, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# -----------------------------------------------------------
# --- Classe principale -------------------------------------
# -----------------------------------------------------------
class Image_devant:
    """Télécharge ou crée une miniature carrée (iTunes → MusicBrainz → secours)."""

    def __init__(self, artiste: str, album: str) -> None:
        # --- Correction spéciale "Artiste - Album" ---
        artiste, album = fusionner_artiste_album(artiste, album)

        self.artiste: str = nettoyer_nom(artiste)
        self.album: str = nettoyer_nom(album)
        self.user_agent: str = "PyCDCover/1.0 (Gérard Le Rest)"
        self.dossier_thumbnails: Path = Path.home() / "PyCDCover" / "thumbnails"
        self.dossier_thumbnails.mkdir(exist_ok=True)
        self.chemin: Path = self.dossier_thumbnails / f"{self.artiste} - {self.album}.jpg"

    # -------------------------------------------------------
    # --- Requêtes réseau ----------------------------------
    # -------------------------------------------------------
    def _recherche_musicbrainz(self) -> Optional[str]:
        """
        Cherche l'ID de release-group MusicBrainz pour (artiste, album).
        Utilise un cache JSON pour éviter les requêtes répétées.
        """
        cache = lire_cache()
        cle = f"{self.artiste}|{self.album}"
        if cle in cache:
            return cache[cle]

        url = "https://musicbrainz.org/ws/2/release-group/"

        def requete(query: str) -> Optional[str]:
            try:
                r = requests.get(
                    url,
                    params={"query": query, "fmt": "json", "limit": 1},
                    headers={"User-Agent": self.user_agent},
                    timeout=8,
                )
                if r.status_code != 200:
                    return None
                data = r.json()
                groupes = data.get("release-groups", [])
                return groupes[0]["id"] if groupes else None
            except Exception:
                return None

        # 1) Recherche précise
        q1 = f'releasegroup:"{self.album}" AND artist:"{self.artiste}"'
        id_release = requete(q1)

        # 2) Recherche simplifiée si la première échoue
        if not id_release:
            q2 = f'releasegroup:"{self.album}"'
            id_release = requete(q2)
            if id_release:
                print(f"⚠ Recherche simplifiée : {self.artiste} – {self.album}")

        # Mise à jour du cache si trouvée
        if id_release:
            cache[cle] = id_release
            ecrire_cache(cache)

        return id_release

    def _telecharger_image(self, url: Optional[str]) -> Optional[bytes]:
        """Télécharge l'image depuis l'URL fournie."""
        if not url:
            return None
        try:
            r = requests.get(
                url,
                headers={"User-Agent": self.user_agent},
                timeout=10,
            )
            if r.status_code == 200:
                return r.content
        except Exception:
            return None
        return None

    # -------------------------------------------------------
    # --- Génération d'image -------------------------------
    # -------------------------------------------------------
    def _image_secours(self) -> Image.Image:
        """
        Crée une image de secours (fond orange + texte artiste/album centré).
        """
        taille = 512
        img = Image.new("RGB", (taille, taille), (255, 140, 0))
        draw = ImageDraw.Draw(img)
        texte = f"{self.artiste}\n{self.album}"
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
        except Exception:
            font = ImageFont.load_default()
        tw, th = draw.multiline_textbbox((0, 0), texte, font=font)[2:]
        draw.multiline_text(
            ((taille - tw) / 2, (taille - th) / 2),
            texte,
            fill="white",
            font=font,
            align="center",
        )
        return img

    def _normaliser_image(self, donnees: bytes) -> Image.Image:
        """
        Ouvre l'image, la convertit en RGB, la met à l'échelle dans un carré 512x512
        avec fond orange et la retourne.
        """
        image = Image.open(io.BytesIO(donnees)).convert("RGB")
        image.thumbnail((512, 512))
        fond = Image.new("RGB", (512, 512), (255, 140, 0))
        x = (512 - image.width) // 2
        y = (512 - image.height) // 2
        fond.paste(image, (x, y))
        return fond

    # -------------------------------------------------------
    # --- Méthode publique ---------------------------------
    # -------------------------------------------------------
    def creer(self, forcer: bool = False) -> Path:
        """
        Crée (ou récupère) la miniature de couverture.

        - Si le fichier existe déjà et forcer=False : on le réutilise.
        - Sinon :
            1) iTunes
            2) MusicBrainz + CoverArtArchive
            3) Image de secours
        """
        if self.chemin.exists() and not forcer:
            return self.chemin

        # 1) iTunes
        image_url = get_itunes_cover(self.artiste, self.album)
        donnees = self._telecharger_image(image_url) if image_url else None

        # 2) MusicBrainz si iTunes a échoué
        if not donnees:
            id_release = self._recherche_musicbrainz()
            if id_release:
                url_mb = f"https://coverartarchive.org/release-group/{id_release}/front"
                donnees = self._telecharger_image(url_mb)

        # 3) Normalisation et sauvegarde
        if donnees:
            try:
                image = self._normaliser_image(donnees)
                image.save(self.chemin, "JPEG", quality=90)
                return self.chemin
            except Exception:
                # On tombe sur l'image de secours en cas de problème
                pass

        image_secours = self._image_secours()
        image_secours.save(self.chemin, "JPEG", quality=90)
        return self.chemin


# -----------------------------------------------------------
# --- Traitement en lot (optimisation multi-thread) ---------
# -----------------------------------------------------------
def creer_lot(
    albums: Iterable[tuple[str, str]],
    max_workers: int = 4,
    forcer: bool = False,
) -> list[Path]:
    """
    Crée les images pour une liste de (artiste, album) en parallèle.

    - albums : iterable de tuples (artiste, album)
    - max_workers : nombre de threads (4 par défaut)
    - forcer : vrai pour régénérer même si le fichier existe déjà

    Renvoie une liste de chemins de fichiers dans le même ordre
    que la liste d'entrée.
    """
    albums_list = list(albums)
    chemins: list[Path] = []

    def _tache(pair: tuple[str, str]) -> Path:
        artiste, album = pair
        return Image_devant(artiste, album).creer(forcer=forcer)

    if not albums_list:
        return chemins

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(_tache, pair) for pair in albums_list]
        for future in futures:
            chemins.append(future.result())

    return chemins


# -----------------------------------------------------------
# --- Test manuel -------------------------------------------
# -----------------------------------------------------------
if __name__ == "__main__":
    # Test unitaire simple
    test = Image_devant("Alt-J - fsdfsd", "")
    print(test.creer())

    # Exemple de traitement en lot
    # res = creer_lot([
    #     ("AC/DC", "Back in Black"),
    #     ("Pulp", "Different Class"),
    #     ("Daft Punk", "Discovery"),
    # ])
    # print(res)

