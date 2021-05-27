from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QGridLayout,
)
from PyQt5.QtGui import (
    QPixmap,
    QBrush,
    QPainter,
)
from PyQt5.QtCore import Qt
from do.libs.helpers import load_qss_for

SIZE = '24px'
FONTSIZE = '10px'
class UserWidget(QWidget):
    def __init__(self, user, avatar_data, parent=None):
        super(UserWidget, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setObjectName(f"user_widget_{user['id']}")
        self.setFixedHeight(26)

        self.avatar_data = avatar_data
        self.speaking = False
        self.user = user

        layout = QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.init_ui()

    def init_ui(self):
        self.nick_label = UserWidgetNickLabel(self.user['nick'], parent=self)
        self.layout().addWidget(self.nick_label, 0, 0)
        if False:
            self.avatar_label = RoundUserWidgetAvatar(avatar=self.avatar_data, parent=self)
        else:
            self.avatar_label = SquareUserWidgetAvatar(avatar=self.avatar_data, parent=self)
        self.layout().addWidget(self.avatar_label, 0, 1)

    def add_deaf_icon(self):
        self.remove_deaf_icon()
        deaf_pixmap = QPixmap(':/images/deaf.png')
        image = QLabel(parent=self)
        image.setObjectName('deaf_user')
        image.setPixmap(deaf_pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.FastTransformation))
        image.setFixedSize(20, 20)
        self.layout().addWidget(image, 0, 1, Qt.AlignRight | Qt.AlignBottom)

    def remove_mute_icon(self):
        for qlabel in self.findChildren(QLabel):
            if qlabel.objectName() == 'mute_user':
                qlabel.setParent(None)

    def update_nickname(self, nickname):
        self.nick_label.setText(nickname)

    def add_mute_icon(self):
        self.remove_mute_icon()
        mute_pixmap = QPixmap(':/images/mute.png')
        image = QLabel(parent=self)
        image.setObjectName('mute_user')
        image.setPixmap(mute_pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.FastTransformation))
        image.setFixedSize(20, 20)
        self.layout().addWidget(image, 0, 1, Qt.AlignRight | Qt.AlignBottom)

    def remove_deaf_icon(self):
        for qlabel in self.findChildren(QLabel):
            if qlabel.objectName() == 'deaf_user':
                qlabel.setParent(None)

    def stop_speaking(self):
        self.speaking = False
        self.setStyleSheet(f'#{self.objectName()}{{border: 0px;}}')

    def start_speaking(self):
        self.speaking = True
        self.setStyleSheet(f'#{self.objectName()}{{border: 2px solid green;}}')

class UserWidgetAvatar(QLabel):
    def __init__(self, avatar, parent):
        super().__init__(parent=parent)
        self.setStyleSheet('padding-right: 2px;border-radius: 14px; background-color: transparent;')
        self.setFixedSize(24, 24)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.avatar_pix = QPixmap()
        self.avatar_pix.loadFromData(avatar)
        self.avatar_pix = self.avatar_pix.scaled(28, 28, Qt.KeepAspectRatio, Qt.FastTransformation)


class RoundUserWidgetAvatar(UserWidgetAvatar):
    def __init__(self, avatar, parent):
        super().__init__(avatar=avatar, parent=parent)

    def paintEvent(self, event):
        brush = QBrush(self.avatar_pix)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setBrush(brush)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), self.width()/2, self.height()/2)
        self.setPixmap(self.avatar_pix)


class SquareUserWidgetAvatar(UserWidgetAvatar):
    def __init__(self, avatar, parent):
        super().__init__(avatar=avatar, parent=parent)
        self.setPixmap(self.avatar_pix)


class UserWidgetNickLabel(QLabel):
    def __init__(self, nickname, parent):
        super().__init__(text=nickname, parent=parent)
        self.setProperty('cssClass', 'UserWidgetNickLabel')
        self.setStyleSheet(load_qss_for('UserWidgetNickLabel'))
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
