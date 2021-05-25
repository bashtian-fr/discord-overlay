import logging

from PyQt5.QtWidgets import QMainWindow

from .main_ui import MainViewUi


class MainView(QMainWindow):
    def __init__(self, controller, model):
        super().__init__()
        self._controller = controller
        self._model = model
        self._ui = MainViewUi()
        self._ui.setupUi(self)

        self._model.users_changed.connect(self.on_user_changed)

    def on_user_changed(self, value):
        logging.debug('redrawing users %s', value)
