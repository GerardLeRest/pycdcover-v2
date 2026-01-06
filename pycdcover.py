"""
# Point d'entrée du logiciel PyCDCover
# Auteur : Gérard Le Rest (2025)
"""

import json
import locale
import gettext
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / "locales"

# lecture de la langue depuis le JSON
with open(BASE_DIR / "configurationLangue.json", "r", encoding="utf-8") as f:
    langue = json.load(f).get("langueSelectionnee", "fr")

# locale système (formats, dates, etc.)
locale.setlocale(locale.LC_ALL, "")

# gettext piloté par la langue applicative
translation = gettext.translation(
    domain="messages",
    localedir=str(LOCALE_DIR),
    languages=[langue],
    fallback=True,   # IMPORTANT
)

translation.install()

# ⬇️ imports UI après gettext
from PySide6.QtWidgets import QApplication
from Controleur.Application import Application


def main():
    app = QApplication([])
    application = Application()
    application.demarrer()
    app.exec()


if __name__ == "__main__":
    main()

