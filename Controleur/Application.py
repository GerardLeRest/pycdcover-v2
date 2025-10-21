from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Slot
import sys, os
from Vue.Fenetre import Fenetre
from Vue.Fen_Titre import Fen_Titre
from Modele.Titres import Titres
import shutil

class Application(QWidget):

    def __init__(self):
        """initialisation"""
        super().__init__()
        self.reinitialiser_dossier_pycdcover()
        self.fenetre = Fenetre()
        self.fenetre.demande_saisie_titre.connect(self.activer_titre)

    def reinitialiser_dossier_pycdcover(self)->None:
        dossier_principal = os.path.expanduser("~/PyCDCover")
        # Supprime complètement le dossier s'il existe
        if os.path.exists(dossier_principal):
            shutil.rmtree(dossier_principal)
        # Le recrée avec le sous-dossier Thumbnails
        chemin = os.path.join(dossier_principal, "Thumbnails")
        if not os.path.exists(chemin):
            os.makedirs(chemin)

    @Slot(bool)
    def activer_titre(self, titre_selec: bool):
        if titre_selec:
            self.fen_titre = Fen_Titre()
            self.fen_titre.titre_selectionne.connect(self.recuperer_titre)
            self.fen_titre.exec()   # ouverture de la fenetre

    @Slot(str)
    def recuperer_titre(self, titre_str: str):
        print(f"Titre reçu : {titre_str}")
        t = Titres(1200, 1380, titre_str)
        self.titre_horizontal = t.titre_horizontal()
        self.encadrements = t.encadrements_titre()
        self.titre_vertical1 = t.titre_vertical1()
        self.titre_vertical2 = t.titre_vertical2()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    appli = Application()
    appli.fenetre.show()  # on affiche la fenêtre principale
    app.exec()