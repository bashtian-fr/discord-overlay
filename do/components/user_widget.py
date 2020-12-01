from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QGridLayout,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class UserWidget(QWidget):
    def __init__(self, user, avatar_data, parent=None):
        super(UserWidget, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setObjectName('user_widget_%s' % user['id'])
        self.setFixedHeight(32)

        self.user = user
        self.avatar_data = avatar_data

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.init_ui()

    def init_ui(self):
        self.nick_label = self.get_nick_lavel()
        self.layout().addWidget(self.nick_label, 0, 0)
        self.avatar_label = self.get_avatar_label()
        self.layout().addWidget(self.avatar_label, 0, 1)

    def get_nick_lavel(self):
        nick_label = QLabel(self.user['nick'], parent=self)
        nick_label.setProperty('cssClass', 'user_widget_nick')
        nick_label.setStyleSheet("""
            QLabel[cssClass="user_widget_nick"] {
                color: white;
                font-size: 14px;
                padding-left: 2px;
            }
        """)
        nick_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        return nick_label

    def get_avatar_label(self):
        avatar_label = QLabel(parent=self)
        avatar_label.setStyleSheet('padding-right: 2px;')
        avatar_label.setFixedSize(28, 28)
        avatar_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        avatar_pix = QPixmap()
        avatar_pix.loadFromData(self.avatar_data)
        avatar_pix = avatar_pix.scaled(28, 28, Qt.KeepAspectRatio, Qt.FastTransformation)
        avatar_label.setPixmap(avatar_pix)

        return avatar_label
