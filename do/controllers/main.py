from PyQt5.QtCore import (
    QObject,
    pyqtSignal,
    pyqtSlot,
)
from PyQt5.QtWidgets import qApp


class MainController(QObject):
    main_window_visibility_changed = pyqtSignal()
    settings_dialog_visibility_changed = pyqtSignal()

    def __init__(self, model):
        super().__init__()
        self._model = model

    @pyqtSlot()
    def quit_app(self):
        qApp.quit()
