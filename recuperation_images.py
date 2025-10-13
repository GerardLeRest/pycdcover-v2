# -----------------------------------------------------------------------------
# Classe générée par ChatGPT selon mes instructions et mes retours sur les bugs.
# Je la considère comme une bibliothèque externe :
# elle gère la récupération ou la création des images des jaquettes.
#
# Cette classe m’aurait demandé trop de temps et d’énergie à écrire seul.
# Je n’ai pas cherché à en comprendre les détours.
# Elle est stable, isolée, et utilisée ici comme un module.
# -----------------------------------------------------------------------------

import os
import io
import re
import textwrap
import requests
from PIL import Image, ImageDraw, ImageFont
from urllib.parse import quote_plus

class Jaquette:
    """
    Récupère une jaquette (MusicBrainz/Cover Art Archive), crée un fallback si non trouvée,
    rend l'image carrée, redimensionne et enregistre dans ./thumbnails.

    IMPORTANT :
    - Aucune normalisation/trim des champs visibles (artiste/album).
    - Les variantes ne servent QUE pour la RECHERCHE interne (MusicBrainz).
    """

    USER_AGENT = "PyCDCover/1.0 (https://github.com/GerardLeRest/pycdcover; contact: gerard.lerest@orange.fr) Python-requests"
    PAYS_PREFERES = ("FR", "GB", "UK", "US", "DE")

    # Qualificatifs courants en fin de titre (utilisés SEULEMENT pour élargir la recherche)
    QUALIFS_PATTERNS = (
        r"\s*[\[(](?:remaster(?:ed)?|remix(?:ed)?|deluxe|expanded|anniversary|special\s+edition|super\s+deluxe|bonus\s+tracks?|mono|stereo|mix|edition|version|reissue|legacy|collector|live(?:\s+at.*?)?|201\d|200\d|19\d{2})[\])]\s*$",
        r"\s*-\s*(?:remaster(?:ed)?|remix(?:ed)?|deluxe|expanded|anniversary|special\s+edition|super\s+deluxe|bonus\s+tracks?|mono|stereo|mix|edition|version|reissue|legacy|collector)\s*$",
    )

    def __init__(self, auteur: str, album: str, taille: int = 512, dossier_vignettes: str = "thumbnails"):
        # Garder les champs tels quels (pas de strip/upper/lower)
        self.auteur = auteur if auteur is not None else ""
        self.album = album if album is not None else ""
        self.taille = int(taille)
        self.dossier_vignettes = dossier_vignettes
        os.makedirs(self.dossier_vignettes, exist_ok=True)

    # ---------- MusicBrainz ----------
    def _chercher_id_groupe_release(self) -> str | None:
        if self.auteur == "" or self.album == "":
            return None
        for titre in self._candidats_recherche_album():
            q = f'releasegroup:"{titre}" AND artist:"{self.auteur}" AND primarytype:album'
            url = f"https://musicbrainz.org/ws/2/release-group/?query={quote_plus(q)}&fmt=json&limit=5"
            try:
                r = requests.get(url, headers={"User-Agent": self.USER_AGENT}, timeout=15)
                r.raise_for_status()
                data = r.json()
                groupes = data.get("release-groups", [])
                if groupes:
                    return groupes[0].get("id")
            except Exception:
                continue
        return None

    def _chercher_id_release(self) -> str | None:
        if self.auteur == "" or self.album == "":
            return None
        for titre in self._candidats_recherche_album():
            q = f'releasegroup:"{titre}" AND artist:"{self.auteur}"'
            url = f"https://musicbrainz.org/ws/2/release-group/?query={quote_plus(q)}&fmt=json&limit=1"
            try:
                r = requests.get(url, headers={"User-Agent": self.USER_AGENT}, timeout=15)
                r.raise_for_status()
                data = r.json()
                groupes = data.get("release-groups", [])
                if groupes:
                    return groupes[0].get("id")
            except Exception:
                continue
        return None

    def _telecharger_octets_jaquette(self, id_release: str) -> bytes | None:
        if not id_release:
            return None
        urls = [
            f"https://coverartarchive.org/release/{id_release}/front-500",
            f"https://coverartarchive.org/release/{id_release}/front",
        ]
        for url in urls:
            try:
                r = requests.get(url, headers={"User-Agent": self.USER_AGENT}, timeout=20)
                if r.status_code == 200 and r.content:
                    return r.content
            except Exception:
                continue
        return None

    def _telecharger_octets_jaquette_groupe(self, id_groupe: str) -> bytes | None:
        if not id_groupe:
            return None
        urls = [
            f"https://coverartarchive.org/release-group/{id_groupe}/front-500",
            f"https://coverartarchive.org/release-group/{id_groupe}/front",
        ]
        for url in urls:
            try:
                r = requests.get(url, headers={"User-Agent": self.USER_AGENT}, timeout=20)
                if r.status_code == 200 and r.content:
                    return r.content
            except Exception:
                continue
        return None

    # ---------- Outils image ----------
    def _ouvrir_image(self, donnees: bytes) -> Image.Image | None:
        try:
            return Image.open(io.BytesIO(donnees)).convert("RGB")
        except Exception:
            return None

    def _rendre_carree(self, image: Image.Image) -> Image.Image:
        largeur, hauteur = image.size
        if largeur == hauteur:
            return image
        cote = max(largeur, hauteur)
        canevas = Image.new("RGB", (cote, cote), (0, 0, 0))
        canevas.paste(image, ((cote - largeur) // 2, (cote - hauteur) // 2))
        return canevas

    def _redimensionner(self, image: Image.Image) -> Image.Image:
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.LANCZOS  # Pillow ancien
        return image.resize((self.taille, self.taille), resample)

    def _creer_image_secours(self) -> Image.Image:
        """Carré orange avec Auteur + Album centrés, police auto-ajustée."""
        image = Image.new("RGB", (self.taille, self.taille), (255, 140, 0))
        draw = ImageDraw.Draw(image)
        texte = f"{self.auteur}\n{self.album}"
        try:
            taille_police = int(self.taille * 0.12)
            font_base = "DejaVuSans-Bold.ttf"
        except Exception:
            taille_police = int(self.taille * 0.10)
            font_base = None
        marge = int(self.taille * 0.08)
        while taille_police > 10:
            try:
                font = ImageFont.truetype(font_base, taille_police) if font_base else ImageFont.load_default()
            except OSError:
                font = ImageFont.load_default()
            lignes = []
            for ligne in texte.split("\n"):
                lignes.extend(textwrap.wrap(ligne, width=40, break_long_words=True) or [ligne])
            rendu = "\n".join(lignes)
            bbox = draw.multiline_textbbox((0, 0), rendu, font=font, align="center", spacing=int(taille_police*0.25))
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            if tw <= (self.taille - 2*marge) and th <= (self.taille - 2*marge):
                break
            taille_police -= 2
        x = (self.taille - tw) / 2
        y = (self.taille - th) / 2
        try:
            draw.multiline_text((x, y), rendu, font=font, fill=(255, 255, 255),
                                align="center", spacing=int(taille_police*0.25),
                                stroke_width=max(1, taille_police//15), stroke_fill=(0, 0, 0))
        except TypeError:
            draw.multiline_text((x+1, y+1), rendu, font=font, fill=(0, 0, 0),
                                align="center", spacing=int(taille_police*0.25))
            draw.multiline_text((x, y), rendu, font=font, fill=(255, 255, 255),
                                align="center", spacing=int(taille_police*0.25))
        return image

    # ---------- Public ----------
    @staticmethod
    def _sanitiser_nom(texte: str) -> str:
        """Ne remplace que les caractères interdits pour le système de fichiers."""
        t = texte if texte is not None else ""
        return re.sub(r'[\\/:\*\?"<>|]', "-", t)

    def nom_fichier(self) -> str:
        """'Artiste - Album.jpg' (album tel que dans tags.txt, sans normalisation)."""
        artiste = self._sanitiser_nom(self.auteur)
        album_brut = self._sanitiser_nom(self.album)
        nom = f"{artiste} - {album_brut}.jpg"
        return os.path.join(self.dossier_vignettes, nom)

    def obtenir_ou_creer_vignette(self, verbose: bool = False) -> str:
        chemin_sortie = self.nom_fichier()
        if os.path.exists(chemin_sortie):
            return chemin_sortie

        donnees = None
        multi_disc = bool(self._detecter_suffixe_disque(self.album))

        if multi_disc:
            # Multi-disque : d'abord release-group (plus tolérant), puis release
            id_groupe = self._chercher_id_groupe_release()
            if verbose: print("release-group:", id_groupe)
            if id_groupe:
                donnees = self._telecharger_octets_jaquette_groupe(id_groupe)
            if not donnees:
                id_release = self._chercher_id_release()
                if verbose: print("release:", id_release)
                if id_release:
                    donnees = self._telecharger_octets_jaquette(id_release)
        else:
            # Classique : release puis release-group
            id_release = self._chercher_id_release()
            if verbose: print("release:", id_release)
            if id_release:
                donnees = self._telecharger_octets_jaquette(id_release)
            if not donnees:
                id_groupe = self._chercher_id_groupe_release()
                if verbose: print("release-group:", id_groupe)
                if id_groupe:
                    donnees = self._telecharger_octets_jaquette_groupe(id_groupe)

        image = self._ouvrir_image(donnees) if donnees else None
        if image is None:
            image = self._creer_image_secours()
        else:
            image = self._rendre_carree(image)
            image = self._redimensionner(image)

        # Forcer JPEG même si l’album se termine par ".png" (rare)
        if chemin_sortie.endswith(".png"):
            chemin_sortie = chemin_sortie[:-4] + ".jpg"

        image.save(chemin_sortie, format="JPEG", quality=90)
        return chemin_sortie

    # ---------- Helpers ----------
    @staticmethod
    def _album_sans_suffixe_disque(titre: str) -> str:
        """Interne (dédup) : retire 'Disc/CD n' ou '(Disc n of m)' pour la recherche."""
        if not titre:
            return ""
        t = re.sub(r"\((?:disc|cd)\s*\d+\s*of\s*\d+\)", "", titre, flags=re.IGNORECASE)
        t = re.sub(r"\b(?:disc|cd)\s*\d+\b", "", t, flags=re.IGNORECASE)
        return t

    @staticmethod
    def _detecter_suffixe_disque(titre: str) -> str:
        """Retourne '-disc-1-of-2' ou '-disc-2' si détecté ; sinon ''."""
        if not titre:
            return ""
        m = re.search(r"\((?:disc|cd)\s*(\d+)\s*of\s*(\d+)\)", titre, flags=re.IGNORECASE)
        if m:
            return f"-disc-{m.group(1)}-of-{m.group(2)}"
        m2 = re.search(r"\b(?:disc|cd)\s*(\d+)\b", titre, flags=re.IGNORECASE)
        if m2:
            return f"-disc-{m2.group(1)}"
        return ""

    @staticmethod
    def _parentheses_normalisees(titre: str) -> str:
        """
        Normalise UNIQUEMENT l'appariement des parenthèses/crochets pour la RECHERCHE :
        remplace [ et ] par ( et ) sans toucher au reste.
        """
        if not titre:
            return titre
        t = titre
        t = re.sub(r"\[", "(", t)
        t = re.sub(r"\]", ")", t)
        return t

    @staticmethod
    def _titre_sans_qualifs(titre: str) -> str:
        """Retire en douceur les qualificatifs de fin (Remastered/Deluxe/…) pour la RECHERCHE."""
        if not titre:
            return ""
        t = titre
        for _ in range(3):
            t_prev = t
            for pat in Jaquette.QUALIFS_PATTERNS:
                t = re.sub(pat, "", t, flags=re.IGNORECASE)
            if t == t_prev:
                break
        return t.strip()

    def _candidats_recherche_album(self) -> list[str]:
        """
        Variantes POUR LA RECHERCHE UNIQUEMENT (jamais utilisées pour le nom du fichier) :
        1) brut ; 2) parenthèses normalisées ; 3) sans Disc/CD ; 4) sans qualificatifs ; 5) combinée.
        """
        titres = []
        brut = self.album
        titres.append(brut)

        norm = self._parentheses_normalisees(brut)
        if norm != brut:
            titres.append(norm)

        sans_disc = self._album_sans_suffixe_disque(norm)
        if sans_disc and sans_disc not in titres:
            titres.append(sans_disc)

        sans_qualifs = self._titre_sans_qualifs(norm)
        if sans_qualifs and sans_qualifs not in titres:
            titres.append(sans_qualifs)

        combi = self._titre_sans_qualifs(sans_disc)
        if combi and combi not in titres:
            titres.append(combi)

        uniques, seen = [], set()
        for t in titres:
            if t and t not in seen:
                uniques.append(t)
                seen.add(t)
        return uniques


# ------------------- fonction “gestion des albums” -------------------

def traiter_albums(tags_path: str = "tags.txt",
                   dossier_vignettes: str = "thumbnails",
                   taille: int = 512,
                   verbose: bool = False) -> list[str]:
    """
    Lit un fichier au format 'C: Artiste' / 'A: Album' (lignes diverses ignorées),
    puis génère chaque jaquette via la classe Jaquette.
    - 'A:' est conservé tel quel pour le nom du fichier (crochets/parenthèses inclus).
    Retourne la liste des chemins générés.
    """
    import sys

    os.makedirs(dossier_vignettes, exist_ok=True)

    try:
        with open(tags_path, "r", encoding="utf-8") as f:
            lignes = [ln.rstrip("\n") for ln in f]
    except FileNotFoundError:
        if verbose:
            print(f"[traiter_albums] Fichier introuvable : {tags_path}", file=sys.stderr)
        return []

    sorties: list[str] = []
    cur_artist = ""
    cur_album  = ""

    def push_current():
        nonlocal cur_artist, cur_album, sorties
        a = cur_artist.strip()
        b = cur_album.strip()
        if a and b:
            if verbose:
                print(f"> {a} — {b}")
            j = Jaquette(auteur=a, album=b, taille=taille, dossier_vignettes=dossier_vignettes)
            chemin = j.obtenir_ou_creer_vignette(verbose=verbose)
            sorties.append(chemin)
        cur_artist = ""
        cur_album  = ""

    for raw in lignes:
        line = raw.strip()
        if not line:
            continue
        if line[:2].lower() == "c:":
            if cur_artist and cur_album:
                push_current()
            cur_artist = line[2:].strip()
            continue
        if line[:2].lower() == "a:":
            cur_album = line[2:].strip()
            continue
        # le reste (année/genre, .jpg attendu, pistes…) est ignoré

    if cur_artist and cur_album:
        push_current()

    if verbose:
        print(f"[traiter_albums] Générés : {len(sorties)} fichier(s) dans '{dossier_vignettes}'")
    return sorties


# ------------------------------- main court -------------------------------
if __name__ == "__main__":
    # Lancement minimal : lit 'tags.txt' et génère tout
    traiter_albums("tags.txt", dossier_vignettes="thumbnails", taille=512, verbose=True)

