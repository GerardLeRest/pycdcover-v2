from PySide6.QtCore import QObject, Signal
from pathlib import Path
from PySide6.QtCore import Slot


class Haut_gauche(QObject): #QObject -> Signal

    album_selectionne = Signal(dict)  # Le signal enverra un dict
    
    def __init__(self):
        super().__init__()
        self.tableau = [] #album de cle  
        self.albums = {}  # on mémorise le dict des albums
        # Chemin absolu vers le fichier tags.txt (depuis la racine du projet)
        self.fichier_tags = Path(__file__).resolve().parent.parent / "tags.txt"

    def charger_depuis_fichier(self) -> dict:
        albums = {}
        if not self.fichier_tags.exists():
            print("Fichier tags.txt introuvable.")
            return []

        with open(self.fichier_tags, encoding="utf-8") as f:
            lignes = [l.strip() for l in f.readlines()]

        artiste = album = None
        annee = genre = couverture = None
        chansons = []

        for ligne in lignes + [""]:  # force l’enregistrement du dernier album
            if ligne.startswith("C:"):
                artiste = ligne[2:].strip()
            elif ligne.startswith("A:"):
                album = ligne[2:].strip()
            elif ligne.lower().endswith((".jpg", ".jpeg", ".png")):
                couverture = ligne.strip()
            elif " - " in ligne:
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
            elif ligne == "":  # fin de bloc album
                if artiste and album:
                    cle = f"{artiste} - {album}"

                    # ✅ Si aucune couverture trouvée, on la déduit automatiquement
                    if not couverture:
                        couverture = f"{artiste} - {album}.jpg"

                    if hasattr(self, "tableau"):
                        self.tableau.append(cle)

                    albums[cle] = {
                        "artiste": artiste,
                        "album": album,
                        "annee": annee,
                        "genre": genre,
                        "couverture": couverture,
                        "chansons": chansons,
                    }

                # reset pour l’album suivant
                artiste = album = annee = genre = couverture = None
                chansons = []

        self.albums = albums
        return albums

    def afficher(self) -> None:
        albums = self.albums  # utilise ceux déjà chargés
        for cle, infos in albums.items():
            print(cle, "=>", infos["annee"], infos["genre"])
            for t in infos["chansons"]:
                print("   ", t["numero"], "-", t["titre"])
            print(infos["couverture"])

    @Slot(str)
    def selectionner_album(self, cle: str) -> None:
        """sélectionné l"""
        infos_album = self.albums.get(cle)
        if infos_album:
            self.album_selectionne.emit(infos_album)

if __name__ == "__main__":
    recup = Haut_gauche()
    recup.charger_depuis_fichier()
    recup.afficher()
