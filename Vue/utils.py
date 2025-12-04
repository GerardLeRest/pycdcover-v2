from PySide6.QtWidgets import QApplication

def centrer_fenetre(self):
    frame = self.frameGeometry()
    screen = QApplication.primaryScreen()   # toujours valide
    center_point = screen.availableGeometry().center()
    frame.moveCenter(center_point)
    self.move(frame.topLeft())