from PyQt5.QtCore import (
    QObject,
    pyqtSlot,
)
from PyQt5.QtWidgets import qApp


class MainController(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model

    @pyqtSlot()
    def quit_app(self):
        qApp.quit()

    @pyqtSlot()
    def show_settings_dialog(self):
        pass
