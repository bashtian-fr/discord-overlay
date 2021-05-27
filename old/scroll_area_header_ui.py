from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QToolButton,
    QWidget,
    QSizeGrip,
)
from PyQt5.QtGui import (
    QIcon,
    QPixmap,
)
from do.libs.helpers import load_qss_for


class ScrollAreaHeaderWidget(QWidget):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(Qt.OpenHandCursor)
        self.setFixedHeight(20)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(load_qss_for(self.__class__.__name__))
        self.setToolTip('Hold left click to move')
        self.init_ui(title)

    def init_ui(self, title):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = OverlayHeaderTitleLabel(title, parent=self)
        self.layout.addWidget(self.title_label)

        self.button_toggle = OverlayHeaderToggleButton(parent=self)
        self.layout.addWidget(self.button_toggle, 1, Qt.AlignRight)

        self.sizegrip = OverlayHeaderSizeGrip(parent=self)
        self.layout.addWidget(self.sizegrip, 0, Qt.AlignRight | Qt.AlignTop)

        self.setLayout(self.layout)

        self.sp_retain = self.sizePolicy()
        self.sp_retain.setRetainSizeWhenHidden(True)
        self.setSizePolicy(self.sp_retain)

    def mousePressEvent(self, event): # pylint: disable=invalid-name
        pass
        # TODO:
        # main_frame = self.parent()
        # main_frame.old_pos = event.globalPos()
        # self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event): # pylint: disable=unused-argument,invalid-name
        self.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event): # pylint: disable=invalid-name
        pass
        # TODO:
        # main_frame = self.parent()
        # delta = QPoint(event.globalPos() - main_frame.old_pos)
        # pos_x = main_frame.x() + delta.x()
        # pos_y = main_frame.y() + delta.y()
        # main_frame.move(pos_x, pos_y)
        # main_frame.old_pos = event.globalPos()


class OverlayHeaderTitleLabel(QLabel):
    def __init__(self, title, parent=None):
        super().__init__(text=title, parent=parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(load_qss_for(self.__class__.__name__))


class OverlayHeaderSizeGrip(QSizeGrip):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(load_qss_for(self.__class__.__name__))
        self.setToolTip('Hold left click to resize')

    def mouseMoveEvent(self, event): # pylint: disable=invalid-name,unused-argument
        # implement mouseMoveEvent to override parent one
        # in order to avoid setting position when dragging window
        pass


class OverlayHeaderToggleButton(QToolButton):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(load_qss_for(self.__class__.__name__))
        self.setToolTip('Hide the frame')
        self.setIcon(QIcon(QPixmap(':/images/hide.png')))
        # TODO:
        # self.clicked.connect(self.parent().parent().toggle)
        self.setCursor(Qt.PointingHandCursor)
