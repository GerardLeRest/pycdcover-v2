from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Slot
import sys
from Vue.Fenetre import Fenetre
from Vue.Fen_Titre import Fen_Titre


class Application(QWidget):

    def __init__(self):
        """initialisation"""
        super().__init__()
        self.fenetre = Fenetre()
        self.fenetre.titre_selectionne.connect(self.activer_titre)

    @Slot(bool)
    def activer_titre(self, titre_selec: bool):
        if titre_selec:
            self.fen_titre = Fen_Titre()
            self.fen_titre.titre_selectionne.connect(self.recuperer_titre)
            self.fen_titre.exec()   # ouverture de la fenetre

    @Slot(str)
    def recuperer_titre(self, titre: str):
        self.titre = titre
        print(f"titre: {titre}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    appli = Application()
    appli.fenetre.show()  # on affiche la fenêtre principale
    app.exec()