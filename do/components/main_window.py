import sys
import logging

from PyQt5.QtCore import (
    QTimer,
    Qt,
)
from PyQt5.QtWidgets import (
    QErrorMessage,
    QMainWindow,
    qApp,
)
from PyQt5.QtGui import QIcon

import do.resources.rc # pylint: disable=unused-import
from do import DEFAULT_DISCORD_CLIENT_ID
from do.components.discord_overlay import DiscordOverlay
from do.components.system_tray import SystemTrayIcon
from do.libs.discord_connector import DiscordConnector
from do.libs.helpers import get_app_settings


class MainWindow(QMainWindow):
    def __init__(self, discord_client_id=None):
        super().__init__()
        self.app_icon = QIcon(':/images/icon.ico')
        self.discord_client_id = None
        self.discord_connector = None
        self.discord_overlay = None
        self.sys_tray_icon = None
        self.timer = None
        self.set_discord_client_id(discord_client_id)
        self.init_ui()
        self.init_discord_connector()

    def set_discord_client_id(self, discord_client_id):
        if discord_client_id:
            get_app_settings().setValue('discord_client_id', discord_client_id)
        else:
            get_app_settings().setValue('discord_client_id', DEFAULT_DISCORD_CLIENT_ID)

        get_app_settings().sync()
        self.discord_client_id = get_app_settings().value(
            'discord_client_id',
            defaultValue=DEFAULT_DISCORD_CLIENT_ID,
            type=str
        )

    def init_ui(self):
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setWindowIcon(self.app_icon)
        self.discord_overlay = DiscordOverlay(parent=self)
        self.sys_tray_icon = SystemTrayIcon(icon=self.app_icon, parent=self)

    def init_discord_connector(self):
        self.discord_connector = DiscordConnector(
            client_id=self.discord_client_id
        )
        # All the signal forwards
        self.discord_connector.comm.authenticated.connect(self.discord_overlay.show)
        self.discord_connector.comm.you_joined_voice_channel_signal.connect(self.discord_overlay.you_joined_voice_channel_signal)
        self.discord_connector.comm.you_left_voice_channel_signal.connect(self.discord_overlay.you_left_voice_channel)
        self.discord_connector.comm.someone_joined_voice_channel_signal.connect(self.discord_overlay.someone_joined_channel)
        self.discord_connector.comm.someone_left_voice_channel_signal.connect(self.discord_overlay.someone_left_channel)
        self.discord_connector.comm.speaking_start_signal.connect(self.discord_overlay.speaking_start_signal)
        self.discord_connector.comm.speaking_stop_signal.connect(self.discord_overlay.speaking_stop_signal)
        self.discord_connector.comm.connection_error.connect(self.connection_error)

        logging.info('Starting connector')
        self.timer = QTimer(qApp)
        self.timer.timeout.connect(self.discord_connector.handle)
        self.timer.start(15)

    def connection_error(self, error):
        self.timer.stop()
        error_dialog = QErrorMessage()
        error_dialog.setWindowTitle('Unable to connect to discord')
        error_dialog.showMessage(error)
        error_dialog.exec_()
        sys.exit(1)
