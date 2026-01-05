#!/usr/bin/env python3

"""
# Point d'entrée du logiciel PyCDCover
# Auteur : Gérard Le Rest (2025)
"""

# chargement de a langue sélectionnée
import sys, json, locale, gettext
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / "locales"

# lecture de la langue depuis le JSON (informationnelle)
with open(BASE_DIR / "configurationLangue.json", "r", encoding="utf-8") as f:
    langue = json.load(f).get("langueSelectionnee", "fr")

# locale système (clé du fonctionnement simple)
locale.setlocale(locale.LC_ALL, "")

# gettext simple, robuste, à la Piveo
gettext.install(
    domain="messages",
    localedir=str(LOCALE_DIR),
)

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
