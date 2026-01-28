from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QProgressBar, QLabel, QFileDialog, QMessageBox
)
from PySide6.QtCore import Signal
from pathlib import Path
from builtins import _

class Progress_tags(QMainWindow):

    tags_termines = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle(_("Extraction des tags MP3..."))
        self.resize(300, 100)
        # interface
        layout = QVBoxLayout()
        self.label = QLabel(_("Prêt à extraire les tags"))
        self.fichier_tags = Path.home() / "PyCDCover" / "tags.txt" # fichier des tags
        self.progress: QProgressBar | None = None
        self.nbre_albums = 0 # nbre albums
        layout.addWidget(self.label)
        self.progress = QProgressBar()
        layout.addWidget(self.progress)
        layout.setContentsMargins(20, 10, 20, 20)  # gauche, haut, droite, bas
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def choisir_dossier_chansons(self):
        """Choisir le dossier des chansons"""
        # fenetre du choix du dossier des albums
        chemin = QFileDialog.getExistingDirectory(self,                                         
                                                    _("Choisir le répertoire des chansons"), _("/media"))
        return chemin
    
    def absence_mp3(self, total: int)->None:
        if total == 0:
                QMessageBox.information(self, _("Aucun MP3"), _("Aucune piste MP3 trouvée."))
                return    
   
    def defilement (self, total: int)->None:
    # barre de progression 1
        self.progress.setRange(0, total)
        self.label.setText(_("Extraction en cours..."))
        QApplication.processEvents()   

    #self.progress.setValue(count)
    #QApplication.processEvents()

    def fermeture_fenetre_progress(self)->None:
        # barre de progression 2
        # indiquent que les tags ont écrits        
        self.tags_termines.emit()
        # Barre de progression
        self.progress.setValue(self.progress.maximum())  # sécurité : barre à 100 %
        QApplication.processEvents()                      # rafraîchissement immédiat
        self.close()               