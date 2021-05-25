from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from do.components.system_tray import SystemTrayIcon
from do.components.discord_overlay import DiscordOverlay
from do.libs.helpers import get_app_settings
from do import DEFAULT_DISCORD_CLIENT_ID


class AppController:
    def __init__(self, app) -> None:
        self.app = app
        self.init_ui()

    def init_ui(self) -> None:
        app_icon = QIcon(':/images/icon.ico')

        self.main_window = QMainWindow()
        self.main_window.setAttribute(Qt.WA_NoSystemBackground)
        self.main_window.setAttribute(Qt.WA_TranslucentBackground)
        self.main_window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.main_window.setWindowIcon(app_icon)
        self.discord_overlay = DiscordOverlay(name=self.app.applicationName(), parent=self.main_window)
        self.system_tray_icon = SystemTrayIcon(icon=app_icon, parent=self.main_window)
        self.system_tray_icon.setVisible(True)
        self.main_window.setCentralWidget(self.discord_overlay)

    def set_discord_client_id(self) -> None:
        self.discord_client_id = get_app_settings().value(
            'discord_client_id',
            type=str
        )
        if not self.discord_client_id:
            self.save_default_discord_client_id()

    def save_default_discord_client_id(self) -> None:
        get_app_settings().setValue('discord_client_id', DEFAULT_DISCORD_CLIENT_ID)
        get_app_settings().sync()
