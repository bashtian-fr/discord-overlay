from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QScrollArea,
    QVBoxLayout,
    QFrame,
    QApplication,
)

from ..libs.helpers import load_qss_for
from .scroll_area_header_ui import ScrollAreaHeaderWidgetUi


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

        self.scroll_area = QScrollArea(parent=self.centralwidget)
        # TODO: move to dedicated object
        self.scroll_area.setObjectName('DiscordOverlayScrollArea')
        self.scroll_area.setStyleSheet(load_qss_for('DiscordOverlayScrollArea'))
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_header = ScrollAreaHeaderWidgetUi(
            parent=self.centralwidget,
            title=QApplication.instance().applicationName(),
        )
        centralwidget_layout.addWidget(self.scroll_area_header)
        centralwidget_layout.addWidget(self.scroll_area)

        self.centralwidget.setLayout(centralwidget_layout)

        main_window.setCentralWidget(self.centralwidget)
