#!/usr/bin/env python3

"""
# PyCDCover - Récupération des images
Ces deux classes sont utilisées comme des bibliothèques.
Je ne cherche pas à en comprendre les détails internes. 
"""

import os, io, re, json, requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from urllib.parse import quote
from typing import Optional, Any


# -----------------------------------------------------------
# --- Fonctions utilitaires ---------------------------------
# -----------------------------------------------------------

def get_itunes_cover(artiste: str, album: str) -> Optional[str]:
    """Recherche la jaquette de l'album sur iTunes et renvoie l'URL haute résolution."""
    try:
        recherche = quote(f"{artiste} {album}")
        url = f"https://itunes.apple.com/search?term={recherche}&entity=album&limit=1"
        r = requests.get(url, timeout=8)
        if r.status_code != 200:
            return None

        data = r.json()
        if data.get("resultCount", 0) <= 0:
            return None

        results = data.get("results", [])
        if not results:
            return None

        image_url = results[0].get("artworkUrl100")
        if not image_url:
            return None

        # On demande une meilleure résolution si possible
        return image_url.replace("100x100bb", "600x600bb")
    except Exception as e:
        print(f"Erreur API iTunes pour {artiste} - {album} : {e}")
    return None


def lire_tags(fichier: str = "tags.txt") -> list[dict[str, Any]]:
    """
    Lit le fichier tags.txt et renvoie une liste de dictionnaires :
    [
        {
            "artiste": "Nom de l'artiste",
            "album": "Titre de l'album",
            "couverture": "Artiste - Album.jpg",
            "image_url": "https://..."
        },
        ...
    ]
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
    """Nettoie les noms d’artistes ou d’albums pour éviter les erreurs d’URL."""
    if not nom:
        return ""
    nom = re.sub(r"[\(\[\{].*?[\)\]\}]", "", nom)
    nom = re.sub(
        r"\b(remaster(ed)?|disc|cd|deluxe|version|edition|bonus|anniversary|remix|mono|stereo)\b",
        "",
        nom,
        flags=re.IGNORECASE,
    )
    nom = re.sub(r"\s{2,}", " ", nom)
    return nom.strip()


def sanitiser_nom_fichier(nom: str, remplacement: str = "_") -> str:
    """
    Nettoie un nom pour l'utiliser comme nom de fichier.

    - Supprime / remplace les caractères problématiques.
    - Coupe si c'est vraiment trop long (sécurité).
    """
    # Caractères interdits sur la plupart des systèmes
    nom = re.sub(r'[<>:"/\\|?*]', remplacement, nom)
    nom = re.sub(r"\s{2,}", " ", nom)
    nom = nom.strip()
    # On limite un peu la longueur pour éviter les soucis extrêmes
    if len(nom) > 180:
        nom = nom[:180]
    return nom


# -----------------------------------------------------------
# --- Gestion du cache JSON ---------------------------------
# -----------------------------------------------------------
CACHE_PATH = Path.home() / "PyCDCover" / "cache.json"


def lire_cache() -> dict[str, str]:
    if CACHE_PATH.exists():
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except Exception:
            # Cache corrompu ou illisible : on repart de zéro
            return {}
    return {}


def ecrire_cache(cache: dict[str, str]) -> None:
    try:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        # En cas d'erreur d'écriture, on ne fait rien (fonction non bloquante).
        pass


# -----------------------------------------------------------
# --- Classe principale -------------------------------------
# -----------------------------------------------------------
class Image_devant:
    """Télécharge ou crée une miniature carrée (iTunes → MusicBrainz → secours)."""

    def __init__(self, artiste: str, album: str) -> None:
        self.artiste: str = nettoyer_nom(artiste)
        self.album: str = nettoyer_nom(album)
        self.user_agent: str = "PyCDCover/1.0 (Gérard Le Rest)"
        self.dossier_thumbnails: Path = Path.home() / "PyCDCover" / "thumbnails"
        self._preparer_dossier_thumbnails()

        nom_fichier: str = sanitiser_nom_fichier(f"{self.artiste} - {self.album}.jpg")
        self.chemin: Path = self.dossier_thumbnails / nom_fichier
        self._cle_cache: str = f"{self.artiste}|{self.album}"

    # -------------------------------------------------------
    # Méthodes internes de préparation / utilitaires
    # -------------------------------------------------------
    def _preparer_dossier_thumbnails(self) -> None:
        """Crée le dossier des miniatures si nécessaire."""
        try:
            self.dossier_thumbnails.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Impossible de créer le dossier des miniatures : {e}")

    def _miniature_existe(self) -> bool:
        """Vérifie si la miniature existe déjà sur le disque."""
        return self.chemin.exists()

    def _telecharger_image(self, url: Optional[str]) -> Optional[bytes]:
        """Télécharge une image à partir d'une URL."""
        if not url:
            return None
        try:
            r = requests.get(
                url,
                headers={"User-Agent": self.user_agent},
                timeout=10
            )
            if r.status_code == 200:
                return r.content
        except Exception:
            return None
        return None

    # -------------------------------------------------------
    # Méthodes liées à MusicBrainz
    # -------------------------------------------------------
    def _recherche_musicbrainz(self) -> Optional[str]:
        """Recherche l’ID du release-group sur MusicBrainz (avec cache)."""
        cache = lire_cache()

        if self._cle_cache in cache:
            return cache[self._cle_cache]

        def requete(query: str) -> Optional[str]:
            url = "https://musicbrainz.org/ws/2/release-group/"
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
                if not groupes:
                    return None
                return groupes[0].get("id")
            except Exception:
                return None

        q1 = f'releasegroup:"{self.album}" AND artist:"{self.artiste}"'
        id_release = requete(q1)

        if not id_release:
            q2 = f'releasegroup:"{self.album}"'
            id_release = requete(q2)
            if id_release:
                print(f"⚠ Recherche simplifiée : {self.artiste} – {self.album}")

        if id_release:
            cache[self._cle_cache] = id_release
            ecrire_cache(cache)

        return id_release

    # -------------------------------------------------------
    # Méthodes de récupération des données d'image
    # -------------------------------------------------------
    def _recuperer_depuis_itunes(self) -> Optional[bytes]:
        """Essaye de récupérer la jaquette via iTunes."""
        image_url = get_itunes_cover(self.artiste, self.album)
        if not image_url:
            return None
        return self._telecharger_image(image_url)

    def _recuperer_depuis_musicbrainz(self) -> Optional[bytes]:
        """Essaye de récupérer la jaquette via MusicBrainz."""
        id_release = self._recherche_musicbrainz()
        if not id_release:
            return None
        url_mb = f"https://coverartarchive.org/release-group/{id_release}/front"
        return self._telecharger_image(url_mb)

    def _obtenir_donnees_image(self) -> Optional[bytes]:
        """
        Essaie successivement de récupérer les données d'image :
        1) iTunes
        2) MusicBrainz
        """
        donnees = self._recuperer_depuis_itunes()
        if donnees:
            return donnees

        donnees = self._recuperer_depuis_musicbrainz()
        if donnees:
            return donnees

        return None

    # -------------------------------------------------------
    # Méthodes de construction / secours d'image
    # -------------------------------------------------------
    def _creer_image_carrée_centrée(self, image_source: Image.Image, taille: int = 512) -> Image.Image:
        """Crée une image carrée en centrant l'image source."""
        image_source = image_source.convert("RGB")
        image_source.thumbnail((taille, taille))

        fond = Image.new("RGB", (taille, taille), (255, 140, 0))
        x = (taille - image_source.width) // 2
        y = (taille - image_source.height) // 2
        fond.paste(image_source, (x, y))
        return fond

    def _image_secours(self) -> Image.Image:
        """Crée une image orange avec artiste et album."""
        taille = 512
        img = Image.new("RGB", (taille, taille), (255, 140, 0))
        draw = ImageDraw.Draw(img)
        texte = f"{self.artiste}\n{self.album}"
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
        except Exception:
            font = ImageFont.load_default()
        bbox = draw.multiline_textbbox((0, 0), texte, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.multiline_text(
            ((taille - tw) / 2, (taille - th) / 2),
            texte,
            fill="white",
            font=font,
            align="center",
        )
        return img

    def _construire_image(self, donnees: Optional[bytes]) -> Image.Image:
        """
        À partir des données binaires éventuelles, construit l'image finale.
        Si les données sont invalides ou absentes, on génère une image de secours.
        """
        if not donnees:
            return self._image_secours()

        try:
            image_source = Image.open(io.BytesIO(donnees))
            return self._creer_image_carrée_centrée(image_source)
        except Exception:
            return self._image_secours()

    # -------------------------------------------------------
    # Méthodes de sauvegarde
    # -------------------------------------------------------
    def _sauvegarder_image(self, image: Image.Image) -> Path:
        """Sauvegarde l'image au bon endroit et retourne le chemin."""
        try:
            image.save(self.chemin, "JPEG", quality=90)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la miniature : {e}")
        return self.chemin

    # -------------------------------------------------------
    # Méthode publique principale
    # -------------------------------------------------------
    def creer(self, forcer: bool = False) -> Path:
        """Crée ou télécharge la miniature carrée et retourne son chemin."""
        if self._miniature_existe() and not forcer:
            return self.chemin

        donnees = self._obtenir_donnees_image()
        image_finale = self._construire_image(donnees)
        return self._sauvegarder_image(image_finale)


# -----------------------------------------------------------
# --- Test manuel -------------------------------------------
# -----------------------------------------------------------

if __name__ == "__main__":
    test = Image_devant("Alt-J", "An Awesome Wave")
    test.creer()

