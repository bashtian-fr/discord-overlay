from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QFrame,
)


from ..widgets import (
    CentralWidgetScrollArea,
    CentralWidgetScrollAreaHeaderWidget,
)

class MainViewUi():
    def setupUi(self, main_window):
        main_window.setAttribute(
            Qt.WA_AlwaysShowToolTips)
        main_window.setAttribute(
            Qt.WA_TranslucentBackground)
        main_window.setAttribute(
            Qt.WA_NoSystemBackground)
        main_window.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowStaysOnTopHint)
        main_window.setMinimumHeight(200)
        main_window.setMinimumWidth(200)
        main_window.setGeometry(0, 0, 200, 200)

        self.centralwidget = QFrame(parent=main_window)
        self.centralwidget.setAttribute(Qt.WA_AlwaysShowToolTips)
        self.centralwidget.setAttribute(Qt.WA_TranslucentBackground)
        self.centralwidget.setAttribute(Qt.WA_NoSystemBackground)

        centralwidget_layout = QVBoxLayout()
        centralwidget_layout.setContentsMargins(0, 0, 0, 0)
        centralwidget_layout.setSpacing(0)

        self.scroll_area = CentralWidgetScrollArea(parent=self.centralwidget)
        self.scroll_area_header = CentralWidgetScrollAreaHeaderWidget(
            parent=self.centralwidget,
        )
        self.scroll_area_header.setToolTip('Hold left click to move')


        centralwidget_layout.addWidget(self.scroll_area_header)
        centralwidget_layout.addWidget(self.scroll_area)

        self.centralwidget.setLayout(centralwidget_layout)

        main_window.setCentralWidget(self.centralwidget)
