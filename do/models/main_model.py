import logging

from PyQt5.QtCore import (
    QObject,
    pyqtSignal,
)


class MainModel(QObject):
    # What am I suppoed to do ?

    # This?
    users_changed = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._users = []

    @property
    def users(self):
        return self._users

    def add_user(self, value):
        logging.debug('adding user %s', value)
        self._users.append(value)
        self.users_changed.emit(self._users)

    def delete_user(self, value):
        logging.debug('deleting user %s', value)
        del self._users[value]
        self.users_changed.emit(self._users)
