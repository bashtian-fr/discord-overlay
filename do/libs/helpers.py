import logging
import sys
import typing
import urllib3

from PyQt5.QtCore import (
    QFile,
    QIODevice,
    QSettings,
    QTextStream,
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    qApp
)

from do import (
    APPLICATION_NAME,
    ORGANIZATION_DOMAIN,
)


def get_url_data(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    return response.data


def load_qss_for(class_name):
    qss_resource = f':/qss/{class_name}.qss'
    stream = QFile(qss_resource)
    if not stream.exists():
        logging.warning('QSS resource "%s" not found.', qss_resource)
        return ''

    stream.open(QIODevice.ReadOnly)
    return QTextStream(stream).readAll()


def get_app_settings():
    settings = QSettings(
        QSettings.IniFormat,
        QSettings.UserScope,
        ORGANIZATION_DOMAIN,
        APPLICATION_NAME
    )
    return settings


def find_main_window() -> typing.Union[QMainWindow, None]:
    app = QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget
    return None


def exit_app(term=None, source=None): # pylint: disable=unused-argument
    main_window = find_main_window()
    if main_window:
        main_window.sys_tray_icon.hide()
    qApp.exit()
    sys.exit()
