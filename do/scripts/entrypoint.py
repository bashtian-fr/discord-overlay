import click
import logging
import signal
import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication

from do import (
    ORGANIZATION_DOMAIN,
    APPLICATION_NAME,
)
from do.components.main_window import MainWindow
from do.libs.helpers import exit_app


logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)


@click.command()
def main():
    signal.signal(signal.SIGINT, exit_app)
    QCoreApplication.setOrganizationDomain(ORGANIZATION_DOMAIN)
    QCoreApplication.setApplicationName(APPLICATION_NAME)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
