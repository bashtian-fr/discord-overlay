from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from ..widgets import (
    CentralWidget,
    CentralWidgetScrollArea,
    CentralWidgetScrollAreaHeaderSizeGripWidget,
    CentralWidgetScrollAreaHeaderTitleWidget,
    CentralWidgetScrollAreaHeaderToggleButtonWidget,
    CentralWidgetScrollAreaHeaderWidget,
    SettingsDialog,
)


class MainViewUi():
    # pylint: disable=attribute-defined-outside-init
    def setup_ui(self, main_window: 'MainView') -> None:
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
        self.settings_dialog = SettingsDialog(parent=main_window)
        self.settings_dialog.show()
        self.centralwidget = CentralWidget(parent=main_window)
        self.scroll_area = CentralWidgetScrollArea(parent=self.centralwidget)
        self.header = CentralWidgetScrollAreaHeaderWidget(
            tooltip='Hold left click to move',
            main_window=main_window,
            parent=self.centralwidget,
        )
        self.header_title = CentralWidgetScrollAreaHeaderTitleWidget(
            QApplication.instance().applicationName(),
            parent=self.header
        )
        self.header_toggle_button = CentralWidgetScrollAreaHeaderToggleButtonWidget(
            parent=self.header
        )

        self.header_resize_grip = CentralWidgetScrollAreaHeaderSizeGripWidget(
            parent=self.header
        )
        self.header.layout().addWidget(self.header_title)
        self.header.layout().addWidget(
            self.header_toggle_button,
            1,
            Qt.AlignRight
        )
        self.header.layout().addWidget(
            self.header_resize_grip,
            0,
            Qt.AlignRight | Qt.AlignTop
        )

        self.centralwidget.layout().addWidget(self.header)
        self.centralwidget.layout().addWidget(self.scroll_area)

        main_window.setCentralWidget(self.centralwidget)
