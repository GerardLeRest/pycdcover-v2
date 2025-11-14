
"""
Point d'entrée du logiciel PyCDCover
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtWidgets import QApplication
from Controleur.Application import Application

def main():
    """Lance l'application PyCDCover."""
    
    app = QApplication([])
    application = Application()   # instancie le contrôleur
    application.demarrer()        # affiche la fenêtre principale
    app.exec()                    # lance la boucle événementielle de Qt

if __name__ == "__main__":
    main()

