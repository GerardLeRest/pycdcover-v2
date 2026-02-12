#!/usr/bin/env python3

"""
pycdecover.py — initialise la lague au démarrage
lance l'appplication
Auteur : Gérard Le Rest (2026)
"""

import locale
import gettext
from pathlib import Path
from Modele.gestion_langue import GestionLangue
import sys

# Gestion de la langue de cette cesssion
BASE_DIR = Path(__file__).resolve().parent # dossier du programme
LOCALE_DIR = BASE_DIR / "locales"

configDir = Path.home() / ".config" / "pycdcover"
configDir.mkdir(parents=True, exist_ok=True)
fichierLangue = configDir / "configurationLangue.json"

gestionLangue = GestionLangue(fichierLangue)
langue = gestionLangue.lire()

locale.setlocale(locale.LC_ALL, "")

translation = gettext.translation(
    domain="messages",
    localedir=str(LOCALE_DIR),
    languages=[langue],
    fallback=True
)
translation.install()

# Démarrage de la fenêtre principale
from PySide6.QtWidgets import QApplication
from Controleur.application import Application

# ------------------------------------- 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    application = Application()
    application.demarrer()
    sys.exit(app.exec())