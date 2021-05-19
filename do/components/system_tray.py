from PyQt5.QtWidgets import (
    QSystemTrayIcon,
    QMenu,
    QAction,
    qApp,
)
from do import APPLICATION_NAME
from do.libs.helpers import get_app_settings


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super(SystemTrayIcon, self).__init__(icon, parent)
        self.setToolTip(APPLICATION_NAME)
        self.init_ui()

    def init_ui(self):
        self._menu = QMenu()

        toggle_overlay_action = QAction(
            '&Toggle the overlay',
            parent=self,
            triggered=self.toggle_overlay
        )
        self._menu.addAction(toggle_overlay_action)

        settings_menu = self._menu.addMenu('&Settings')
        show_only_speakers = QAction(
            '&Only Speakers',
            parent=self,
            triggered=self.show_only_speakers_callback,
            checkable=True,
            checked = get_app_settings().value('show_only_speakers', defaultValue=False, type=bool)
        )
        settings_menu.addAction(show_only_speakers)

        quit_action = QAction('&Exit', parent=self, triggered=self.exit)
        self._menu.addAction(quit_action)

        self.setContextMenu(self._menu)
        self.show()

    def toggle_overlay(self):
        self.parent().discord_overlay.toggle()

    def show_only_speakers_callback(self, checked):
        get_app_settings().setValue('show_only_speakers', checked)
        dicord_overlay = self.parent().discord_overlay
        if checked:
            dicord_overlay.hide_all_users()
        else:
            dicord_overlay.show_all_users()

    def exit(self):
        qApp.quit()
