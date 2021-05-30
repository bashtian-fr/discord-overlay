import logging
from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
)

from .main_ui import MainViewUi
from ..models import MainModel
from ..controllers import MainController


class MainView(QMainWindow):
    def __init__(self, controller: MainController, model: MainModel) -> None:
        super().__init__()
        self._controller = controller
        self._model = model
        self._ui = MainViewUi()
        self._ui.setup_ui(self)
        self.old_pos = self.pos()
        self._ui.header_toggle_button.clicked.connect(self.toggle)
        self._model.users_changed.connect(self.on_users_changed)
        self._controller.main_window_visibility_changed.connect(self.toggle)
        self._controller.settings_dialog_visibility_changed.connect(self.toggle_settings)

    def on_users_changed(self, value):
        logging.debug('redrawing users %s', value)

    def toggle(self):
        if self._ui.header.isVisible():
            self._ui.header.hide()
            self._ui.scroll_area.hide_border()
            app = QApplication.instance()
            if app.system_tray_view.supportsMessages():
                app.system_tray_view.showMessage(
                    app.applicationName(),
                    f'The {app.applicationName()} is running in background',
                    QIcon(':/images/icon.ico'),
                    msecs=3000
                )
        else:
            self._ui.header.show()
            self._ui.scroll_area.show_border()

    def toggle_settings(self):
        self._ui.settings_dialog.show()
