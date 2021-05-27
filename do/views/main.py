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
        self.old_pos = self.pos()
        self._model.users_changed.connect(self.on_users_changed)

    def on_users_changed(self, value):
        logging.debug('redrawing users %s', value)
