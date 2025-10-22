from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
import os

class Titres:

    def __init__(self, L_devant, H_back_cover,titre):
        self.titre = titre
        self.L_devant = L_devant
        self.H_back_cover = H_back_cover
        self.x = 0 # position x de l'élément à placer
        self.y = 0 # position y de l'élément à placer
        # création du dossier de travail "dossier_utilisateur"
        # Dossier utilisateur (multiplateforme)
        dossier_utilisateur = Path.home()
        # Dossier de travail de l'appli
        self.dossier_pycovercd = dossier_utilisateur / "PyCDCover"
        # Création automatique s’il n’existe pas - sécurité
        self.dossier_pycovercd.mkdir(exist_ok=True)
        # Se déplacer dans le dossier
        os.chdir(self.dossier_pycovercd)
        
    def titre_horizontal(self):
        """Création de l'image horizontale du titre"""
        print("titre_horizontal")
        # Créer l'image blanche
        self.imageH = Image.new("RGB", (self.L_devant, 220), "white")
        self.draw = ImageDraw.Draw(self.imageH)
        # Police
        police1 = os.path.join(self.dossier_pycovercd, "polices", "FreeSerif.ttf")
        taille = 60
        self.font1 = ImageFont.truetype(police1, taille)
        # Calcul du centrage
        bbox = self.draw.textbbox((0, 0), self.titre, font=self.font1)
        largeur_texte = bbox[2] - bbox[0]
        self.x = (self.L_devant - largeur_texte) / 2
        self.y = 60
        # Dessiner le texte
        self.draw.text((self.x, self.y), self.titre, fill="black", font=self.font1)
        # Sauvegarder après le dessin
        chemin_image = self.dossier_pycovercd / "TitreH.png"
        self.imageH.save(chemin_image, "PNG")
        return self.imageH

    def encadrements_titre(self) -> Image.Image:
        """Création de l'encadrement du titre horizontal"""
        # tracé de cinq rectangles = rectangle intérieur épais
        for e in range(4):
            bbox = self.draw.textbbox((self.x, self.y), self.titre, font=self.font1)
            self.draw.rectangle(
                [(bbox[0]-10-e, bbox[1]-10-e), (bbox[2]+10+e, bbox[3]+10+e)],
                outline="#4e3728"
            )
        # Tracé du rectangle extérieur
        bbox = self.draw.textbbox((self.x, self.y), self.titre, font=self.font1)
        self.draw.rectangle(
            [(bbox[0]-16, bbox[1]-16), (bbox[2]+16, bbox[3]+16)],
            outline="#4e3728"
        )
        # Sauvegarde après ajout des encadrements
        chemin_image = self.dossier_pycovercd / "TitreH.png"
        self.imageH.save(chemin_image, "PNG")
        return self.imageH


    def titre_vertical1(self) -> Image.Image:
        """Création du premier titre vertical"""
        self.imageV = Image.new("RGB", (self.H_back_cover, 60), "white")
        self.draw = ImageDraw.Draw(self.imageV)
        police1 = os.path.join(self.dossier_pycovercd, "polices", "FreeSerif.ttf")
        self.font1 = ImageFont.truetype(police1, 40)
        self.draw.text((40, 5), self.titre, fill="black", font=self.font1)

        out1 = self.imageV.rotate(90, expand=True)
        chemin_image = self.dossier_pycovercd / "TitreV1.png"
        out1.save(chemin_image, "PNG")
        return out1


    def titre_vertical2(self) -> Image.Image:
        """Création du deuxième titre vertical"""
        out2 = self.imageV.rotate(270, expand=True)
        chemin_image = self.dossier_pycovercd / "TitreV2.png"
        out2.save(chemin_image, "PNG")
        return out2

if __name__ =="__main__":
    titre = Titres(1200, 1380, "Titre1")
    titre_horizontal = titre.titre_horizontal()
    encadrements_titre = titre.encadrements_titre()
    titre_vertical = titre.titre_vertical1()
    titre_vertical2 = titre.titre_vertical2()