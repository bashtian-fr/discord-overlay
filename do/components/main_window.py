
import sys
import time
import queue
import logging

from pathlib import Path

from PyQt5.QtCore import (
    Qt,
    QTimer,
    QThreadPool,
)
from PyQt5.QtWidgets import (
    QMainWindow,
    qApp,
    QErrorMessage,
)
from PyQt5.QtGui import QIcon

import do.resources.rc
from do import ORGANIZATION_DOMAIN, APPLICATION_NAME
from do.components.system_tray import SystemTrayIcon
from do.components.discord_overlay import DiscordOverlay
from do.libs.discord_connector import DiscordConnector


class MainWindow(QMainWindow):
    def __init__(self, discord_client_id='207646673902501888'):
        super(MainWindow, self).__init__()
        self.discord_client_id = discord_client_id
        self.title = 'DisordOverlay'
        self.app_icon = QIcon(':/images/icon.ico')
        self.sys_tray_icon = None
        self.discord_overlay = None
        self.discord_connector = None
        self.timer = None
        self.init_ui()
        self.init_discord_connector()

    def init_ui(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setWindowIcon(self.app_icon)
        self.sys_tray_icon = SystemTrayIcon(icon=self.app_icon, parent=self)

        self.discord_overlay = DiscordOverlay(parent=self)

    def init_discord_connector(self):
        self.discord_connector = DiscordConnector(
            client_id=self.discord_client_id,
            discord_overlay=self.discord_overlay
        )

        self.discord_connector.comm.authenticated.connect(self.discord_overlay.launch)
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
