#!/usr/bin/env python3
"""
# PyCDCover - Classe : RecupImagesAvant
# Auteur principal : GPT-5
# Supervision, direction et résolution des incohérences : Gérard Le Rest
"""

import os, io, re, json, requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from urllib.parse import quote


# -----------------------------------------------------------
# --- Fonctions utilitaires ---------------------------------
# -----------------------------------------------------------

def get_itunes_cover(artiste: str, album: str) -> str | None:
    """Recherche la jaquette de l'album sur iTunes et renvoie l'URL haute résolution."""
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


def lire_tags(fichier="tags.txt"):
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


def nettoyer_nom(nom):
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
    nom = re.sub(r"[-_]+", " ", nom)
    nom = re.sub(r"\s{2,}", " ", nom)
    return nom.strip()


# -----------------------------------------------------------
# --- Gestion du cache JSON ---------------------------------
# -----------------------------------------------------------
CACHE_PATH = Path.home() / "PyCDCover" / "cache.json"

def lire_cache():
    if CACHE_PATH.exists():
        try:
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def ecrire_cache(cache):
    try:
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# -----------------------------------------------------------
# --- Classe principale -------------------------------------
# -----------------------------------------------------------
class Image_devant:
    """Télécharge ou crée une miniature carrée (iTunes → MusicBrainz → secours)."""

    def __init__(self, artiste, album):
        self.artiste = nettoyer_nom(artiste)
        self.album = nettoyer_nom(album)
        self.user_agent = "PyCDCover/1.0 (Gérard Le Rest)"
        self.dossier_thumbnails = Path.home() / "PyCDCover" / "thumbnails"
        self.dossier_thumbnails.mkdir(exist_ok=True)
        self.chemin = self.dossier_thumbnails / f"{self.artiste} - {self.album}.jpg"

    def _recherche_musicbrainz(self):
        """Recherche l’ID du release-group sur MusicBrainz (avec cache)."""
        cache = lire_cache()
        cle = f"{self.artiste}|{self.album}"
        if cle in cache:
            return cache[cle]

        def requete(query):
            url = "https://musicbrainz.org/ws/2/release-group/"
            try:
                r = requests.get(
                    url,
                    params={"query": query, "fmt": "json", "limit": 1},
                    headers={"User-Agent": self.user_agent},
                    timeout=8,
                )
                data = r.json()
                groupes = data.get("release-groups", [])
                return groupes[0]["id"] if groupes else None
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
            cache[cle] = id_release
            ecrire_cache(cache)

        return id_release

    def _telecharger_image(self, url):
        """Télécharge une image à partir d'une URL."""
        try:
            r = requests.get(url, headers={"User-Agent": self.user_agent}, timeout=10)
            if r.status_code == 200:
                return r.content
        except Exception:
            return None
        return None

    def _image_secours(self):
        """Crée une image orange avec artiste et album."""
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
                            texte, fill="white", font=font, align="center")
        return img

    def creer(self, forcer=False):
        """Crée ou télécharge la miniature carrée et retourne son chemin."""
        if self.chemin.exists() and not forcer:
            print(f"✔ Déjà présent : {self.chemin.name}")
            return self.chemin

        # 1️⃣ Essayer via iTunes
        image_url = get_itunes_cover(self.artiste, self.album)
        donnees = self._telecharger_image(image_url) if image_url else None

        # 2️⃣ Sinon, fallback via MusicBrainz
        if not donnees:
            id_release = self._recherche_musicbrainz()
            if id_release:
                url_mb = f"https://coverartarchive.org/release-group/{id_release}/front"
                donnees = self._telecharger_image(url_mb)

        # 3️⃣ Si toujours rien → image de secours
        if donnees:
            try:
                image = Image.open(io.BytesIO(donnees)).convert("RGB")
                image.thumbnail((512, 512))
                fond = Image.new("RGB", (512, 512), (255, 140, 0))
                x = (512 - image.width) // 2
                y = (512 - image.height) // 2
                fond.paste(image, (x, y))
                fond.save(self.chemin, "JPEG", quality=90)
                print(f"✓ Image enregistrée : {self.chemin.name}")
                return self.chemin
            except Exception:
                pass

        image = self._image_secours()
        image.save(self.chemin, "JPEG", quality=90)
        print(f"⚠ Jaquette de secours : {self.chemin.name}")
        return self.chemin


# -----------------------------------------------------------
# --- Test manuel -------------------------------------------
# -----------------------------------------------------------
if __name__ == "__main__":
    test = Image_devant("Alt-J", "An Awesome Wave")
    test.creer()
