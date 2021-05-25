from PyQt5.QtWidgets import QApplication

from .controllers import MainController
from .models import MainModel
from .views import (
    SystemTrayView,
    MainView,
)
from .resources import preload as preload_resources


class App(QApplication):
    def __init__(self, organization_domain, application_name):
        super().__init__([])
        preload_resources()
        self.setQuitOnLastWindowClosed(False)
        self.setOrganizationDomain(organization_domain)
        self.setApplicationName(application_name)
        self.model = MainModel()
        self.main_controller = MainController(self.model)
        self.system_tray_view = SystemTrayView(
            controller=self.main_controller,
            model=self.model,
            application_name=application_name,
        )
        self.main_view = MainView(
            controller=self.main_controller,
            model=self.model,
        )
        self.main_view.show()
