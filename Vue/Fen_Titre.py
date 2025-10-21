from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QApplication, QPushButton,
    QHBoxLayout, QLineEdit, QDialog,QMessageBox )
import sys
from PySide6.QtCore import Signal


class Fen_Titre(QDialog):

    titre_selectionne = Signal(str)

    def __init__(self):
        super().__init__()
        self.titre="" # titre du cd
        self.initialiser()

    def initialiser(self)->None:
        """construction de la fenêtre"""
        self.setWindowTitle("Titre du CD")            
        layoutV = QVBoxLayout()
        layoutV.setContentsMargins(20, 20, 20, 20)

        # label
        label = QLabel ("Saisir le titre du CD", self)
        label.setStyleSheet("font-size: 15px; padding: 14px 0;")
        layoutV.addWidget(label)
        
        # layout Horizontal
        layoutH =QHBoxLayout()
        # champ
        self.champ = QLineEdit()
        self.champ.setPlaceholderText("Titre du CD")
        self.champ.setStyleSheet("""
                border: 1px solid #6b5e4f;
                border-radius: 8px;
                padding: 6px 16px;
                margin-right: 20px
                             """)
        layoutH.addWidget(self.champ)
        # bouton
        bouton = QPushButton("Ok", self)
        bouton.setStyleSheet("""
                color: #4e3728;
                border: 1px solid #ffaa43;
                padding: 6px 16px;
                border-radius: 8px;""")
        # accept (QDialog): fereme la fenêtre
        # fixe le code de retour à QDialog.Accepted
        # fait sortir la boucle d’événement de exec()
        # accept -> if dialog.exec vaut True
        bouton.clicked.connect(self.emission_titre)
        layoutH.addWidget(bouton)
        layoutV.addLayout(layoutH)

        self.setLayout(layoutV)

    def emission_titre (self):
        """vérifie la validité du champ"""
        if not self.champ.text():
            QMessageBox.warning(self, "Erreur", "Le champ est vide.")
            return
        elif len(self.champ.text())>15:
            QMessageBox.warning(self, "Erreur", "Le titre est trop long (<16c).")
            return
        else:
            # on doit émettre avant la fermeture de la fenetre
            self.titre_selectionne.emit(self.champ.text())
            self.accept()

    def recup_titre(self):
        """Renvoie le titre saisi"""
        return self.titre

if __name__ == "__main__":
    application = QApplication(sys.argv)
    dialog = Fen_Titre() # dialog: convention Qt pour une fenetre
    if dialog.exec():  # fenêtre modale
        print("Titre saisi :", dialog.recup_titre())  # OK : maintenant ça retourne une str
    else:
        print("Annulé.")
    # on peut quitter proprement (évite de bloquer sur application.exec())
    sys.exit(0)

