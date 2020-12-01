from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QFrame,
)


class Overlay(QFrame):
    def __init__(self, name, pos_x, pos_y, width, height, parent=None):
        super(Overlay, self).__init__(parent)
        self.name = name
        self.title = name
        self._gripSize = 4
        self.setObjectName = self.name
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowStaysOnTopHint
        )

        self.setMinimumHeight(height)
        self.setMinimumWidth(width)
        self.setGeometry(pos_x, pos_y, self.width(), self.height())
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
