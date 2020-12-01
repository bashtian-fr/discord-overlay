from PyQt5.QtCore import (
    Qt,
    QPoint,
)
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QSizeGrip,
    QHBoxLayout,
    QToolButton,
)
from PyQt5.QtGui import (
    QPixmap,
    QIcon,
)


class OverlayHeaderWidget(QWidget):
    def __init__(self, parent, title):
        super(OverlayHeaderWidget, self).__init__(parent)
        self.setObjectName('OverlayHeaderWidget')
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setToolTip('Move')
        self.setStyleSheet('''
            #OverlayHeaderWidget {
                background: #f55742;
            }
        ''')

        self.setFixedHeight(20)
        self.setCursor(Qt.OpenHandCursor)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.label_name = self.get_label_name(title)
        self.layout.addWidget(self.label_name)

        self.button_toggle = self.get_toggle_button()
        self.layout.addWidget(self.button_toggle)

        self.sizegrip = self.get_grip()
        self.layout.addWidget(self.sizegrip, 0, Qt.AlignRight | Qt.AlignTop)

        self.setLayout(self.layout)
        self.sp_retain = self.sizePolicy()
        self.sp_retain.setRetainSizeWhenHidden(True)
        self.setSizePolicy(self.sp_retain)

    def get_label_name(self, title):
        label_name = QLabel(text=title, parent=self)
        label_name.setStyleSheet('padding-left: 2px; border: 0px;')
        return label_name

    def get_grip(self):
        sizegrip = QSizeGrip(self)
        sizegrip.setToolTip('Resize')
        sizegrip.setStyleSheet('''
            QSizeGrip {
                border-image: url(:/images/grip.png);
                background-repeat: no-repeat;
                background-position: center;
                width: 20px;
                height: 20px;
            }
        ''')
        return sizegrip

    def get_toggle_button(self):
        button_toggle = QToolButton(parent=self)

        button_toggle_pixmap = QPixmap(':/images/hide.png')
        button_toggle_icon= QIcon(button_toggle_pixmap)

        button_toggle.setIcon(button_toggle_icon)
        button_toggle.setToolTip('Hide the frame')
        button_toggle.clicked.connect(self.parent().toggle)
        button_toggle.setCursor(Qt.PointingHandCursor)

        return button_toggle

    def mousePressEvent(self, event):
        main_frame = self.parent()
        main_frame.old_pos = event.globalPos()
        self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event):
        main_frame = self.parent()
        delta = QPoint(event.globalPos() - main_frame.old_pos)
        x = main_frame.x() + delta.x()
        y = main_frame.y() + delta.y()
        main_frame.move(x, y)
        main_frame.old_pos = event.globalPos()
