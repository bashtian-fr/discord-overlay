from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMenu,
    QAction
)


class SystemTrayViewUi():
    # pylint: disable=attribute-defined-outside-init
    def setupUi(self, system_tray, application_name):
        system_tray.setToolTip(application_name)
        system_tray.setIcon(QIcon(':/images/icon.ico'))
        system_tray.setVisible(True)

        self.menu = QMenu()
        self.toggle_overlay_action = \
            QAction('&Toggle the overlay', parent=self.menu)
        self.settings_action = QAction('&Settings',parent=self.menu)
        self.quit_action = QAction('&Exit',parent=self.menu)

        self.menu.addAction(self.toggle_overlay_action)
        self.menu.addAction(self.settings_action)
        self.menu.addAction(self.quit_action)

        system_tray.setContextMenu(self.menu)
