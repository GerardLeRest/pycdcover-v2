from PySide6.QtWidgets import QApplication

def CentrerFenetre(self):
    frame = self.frameGeometry()
    ecran = QApplication.primaryScreen()   # toujours valide
    point_central = ecran.availableGeometry().center()
    frame.moveCenter(point_central)
    self.move(frame.topLeft())