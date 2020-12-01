import sys
import typing
import urllib3
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    qApp
)


class ImageGetter:
    def from_url(self, url):
        http = urllib3.PoolManager()
        r = http.request('GET', url)
        return r.data


def findMainWindow() -> typing.Union[QMainWindow, None]:
    app = QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget
    return None


def exit_app(term, source):
    main_window = findMainWindow()
    if main_window:
        main_window.sys_tray_icon.hide()
    qApp.exit()
    sys.exit()
