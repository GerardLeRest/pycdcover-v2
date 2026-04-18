#!/usr/bin/env python3

"""
Bas.py - centrage d'une fenêtre
Auteur : Gérard Le Rest (2025)
"""

from PySide6.QtWidgets import QApplication

def centrage_fenetre(self):
    """centrage de la fenêtre"""
    frame = self.frameGeometry()
    ecran = QApplication.primaryScreen()   # toujours valide
    point_central = ecran.availableGeometry().center()
    frame.moveCenter(point_central)
    self.move(frame.topLeft())