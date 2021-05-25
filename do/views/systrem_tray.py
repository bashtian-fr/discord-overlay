from PyQt5.QtWidgets import QSystemTrayIcon

from .system_tray_ui import SystemTrayViewUi


class SystemTrayView(QSystemTrayIcon):
    def __init__(self, controller, model, application_name):
        super().__init__()
        self._controller = controller
        self._model = model
        self._ui = SystemTrayViewUi()
        self._ui.setupUi(self, application_name)
        self._ui.quit_action.triggered.connect(self._controller.quit_app)
        self._ui.settings_action.triggered.connect(self._controller.show_settings_dialog)
