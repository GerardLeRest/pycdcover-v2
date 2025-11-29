from PySide6.QtWidgets import QWidget

def centrer_fenetre(widget: QWidget) -> None:
    """Centre un QWidget ou QMainWindow sur son écran, sans QApplication."""
    screen_geo = widget.screen().availableGeometry()
    win_geo = widget.frameGeometry()

    x = screen_geo.x() + (screen_geo.width() - win_geo.width()) // 2
    y = screen_geo.y() + (screen_geo.height() - win_geo.height()) // 2

    widget.move(x, y)