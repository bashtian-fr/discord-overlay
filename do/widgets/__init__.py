from PyQt5.QtCore import (
    Qt,
    QPoint,
)
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QToolButton,
    QWidget,
    QSizeGrip,
    QScrollArea,
    QApplication,
)
from PyQt5.QtGui import (
    QIcon,
    QPixmap,
)

from ..libs.helpers import load_qss_for


class CentralWidgetScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(load_qss_for(self.__class__.__name__))
        self.setWidgetResizable(True)


class CentralWidgetScrollAreaHeaderWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(load_qss_for(self.__class__.__name__))
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(Qt.OpenHandCursor)
        self._ui = CentralWidgetScrollAreaHeaderWidgetUi()
        self._ui.setupUi(self)

    def mousePressEvent(self, event): # pylint: disable=invalid-name
        main_frame = self.parent().parent()
        main_frame.old_pos = event.globalPos()
        self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event): # pylint: disable=unused-argument,invalid-name
        self.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event): # pylint: disable=invalid-name
        main_frame = self.parent().parent()
        delta = QPoint(event.globalPos() - main_frame.old_pos)
        pos_x = main_frame.x() + delta.x()
        pos_y = main_frame.y() + delta.y()
        main_frame.move(pos_x, pos_y)
        main_frame.old_pos = event.globalPos()


class CentralWidgetScrollAreaHeaderWidgetUi:
    def setupUi(self, widget):
        widget.layout = QHBoxLayout()
        widget.layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = CentralWidgetScrollAreaHeaderTitleWidget(
            QApplication.instance().applicationName(),
            parent=widget
        )
        widget.layout.addWidget(self.title_label)

        self.button_toggle = CentralWidgetScrollAreaHeaderToggleButtonWidget(parent=widget)
        widget.layout.addWidget(self.button_toggle, 1, Qt.AlignRight)

        self.sizegrip = CentralWidgetScrollAreaHeaderSizeGripWidget(parent=widget)
        widget.layout.addWidget(self.sizegrip, 0, Qt.AlignRight | Qt.AlignTop)

        widget.setLayout(widget.layout)

        sp_retain = widget.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        widget.setSizePolicy(sp_retain)




class CentralWidgetScrollAreaHeaderTitleWidget(QLabel):
    def __init__(self, title, parent=None):
        super().__init__(text=title, parent=parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(load_qss_for(self.__class__.__name__))


class CentralWidgetScrollAreaHeaderSizeGripWidget(QSizeGrip):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(load_qss_for(self.__class__.__name__))
        self.setToolTip('Hold left click to resize')

    def mouseMoveEvent(self, event): # pylint: disable=invalid-name,unused-argument
        # implement mouseMoveEvent to override parent one
        # in order to avoid setting position when dragging window
        pass


class CentralWidgetScrollAreaHeaderToggleButtonWidget(QToolButton):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(load_qss_for(self.__class__.__name__))
        self.setToolTip('Hide the frame')
        self.setIcon(QIcon(QPixmap(':/images/hide.png')))
        # TODO:
        # self.clicked.connect(self.parent().parent().toggle)
        self.setCursor(Qt.PointingHandCursor)
