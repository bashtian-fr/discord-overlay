from PyQt5.QtWidgets import (
    QSystemTrayIcon,
    QMenu,
    QAction,
    qApp,
)


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super(SystemTrayIcon, self).__init__(icon, parent)
        self.setToolTip('Discord-Overlay')
        self.init_ui()

    def init_ui(self):
        self._menu = QMenu()

        toggle_overlay_action = QAction('Toggle the overlay', parent=self, triggered=self.toggle_overlay)
        self._menu.addAction(toggle_overlay_action)

        quit_action = QAction('&Exit', parent=self, triggered=self.exit)
        self._menu.addAction(quit_action)

        self.setContextMenu(self._menu)
        self.show()

    def toggle_overlay(self):
        self.parent().discord_overlay.toggle()

    def exit(self):
        qApp.quit()
