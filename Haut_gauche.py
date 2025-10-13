from PySide6.QtCore import QObject, Signal


class Haut_gauche(QObject): #QObject -> Signal

    album_selectionne = Signal(dict)  # Le signal enverra un dict
    
    def __init__(self):
        super().__init__()
        self.tableau = [] #album de cle  
        self.albums = {}  # on mémorise le dict des albums

    def charger_depuis_fichier(self, fichier_txt: str) -> dict:
        albums = {}
        with open(fichier_txt, encoding="utf-8") as f:
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
                left, right = ligne.split(" - ", 1) # séparation en deux
                left, right = left.strip(), right.strip() # enlever les espaces

                if left.isdigit() and len(left) == 4:
                    # ex:1992
                    try:
                        annee = int(left)
                    except ValueError:
                        annee = None
                    genre = right or None
                else:
                    # "1 - Titre" (piste) ou "Inconnue - Inconnu"
                    try:
                        num = int(left)
                        chansons.append({"numero": num, "titre": right})
                    except ValueError:
                        annee = None
                        genre = right or None
            elif ligne == "":  # fin de bloc album
                if artiste and album:
                    cle = f"{artiste} - {album}"
                    if hasattr(self, "tableau"):
                        self.tableau.append(cle)  # pour un QListWidget par ex.
                    albums[cle] = {
                        "artiste": artiste,
                        "album": album,
                        "annee": annee,
                        "genre": genre,
                        "couverture": couverture,
                        "chansons": chansons,
                    }
                # reset pour le prochain bloc
                artiste = album = None
                annee = genre = couverture = None
                chansons = []

        self.albums = albums  # utile pour l’UI
        return albums

    def afficher(self) -> None:
        albums = self.albums  # utilise ceux déjà chargés
        for cle, infos in albums.items():
            print(cle, "=>", infos["annee"], infos["genre"])
            for t in infos["chansons"]:
                print("   ", t["numero"], "-", t["titre"])
            print(infos["couverture"])


if __name__ == "__main__":
    recup = Haut_gauche()
    recup.charger_depuis_fichier("tags.txt")
    recup.afficher()
