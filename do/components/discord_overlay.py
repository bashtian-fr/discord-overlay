import logging

from PyQt5.QtCore import (
    Qt,
    QTimer,
    QPoint
)
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
)
from PyQt5.QtGui import QPixmap
from do.components.overlay import Overlay
from do.components.overlay_header import OverlayHeaderWidget
from do.libs.helpers import ImageGetter
from do.components.user_widget import UserWidget

class DiscordOverlay(Overlay):
    def __init__(self, parent):
        super(DiscordOverlay, self).__init__(name='DiscordOverlay', pos_x=0, pos_y=0, width=200, height=200, parent=parent)
        self.image_getter = ImageGetter()
        self.setAttribute(Qt.WA_AlwaysShowToolTips)
        self.is_visible = True
        self.header_widget = None
        self.content_widget = None
        self.users = {}
        self.avatars = {}
        self.default_avatar = self.get_avatar('def')
        self.add_header()
        self.add_content_widget_layout()

    def launch(self):
        self.show()
        #QTimer.singleShot(3000, self.activate_bg)


    def activate_bg(self):
        self.parent().sys_tray_icon.showMessage('Discord Overlay', 'Hidding the frame but running in background.\nSee the Menu (Right click) to move/resize')
        self.toggle()

    def add_header(self):
        self.header_widget = OverlayHeaderWidget(parent=self, title=self.name)
        self.layout.addWidget(self.header_widget)
        self.header_widget.show()

    def add_content_widget_layout(self):
        self.content_layout = QVBoxLayout()
        self.content_layout.setDirection(QVBoxLayout.BottomToTop)
        self.content_layout.setAlignment(Qt.AlignTop)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        self.content_widget = QWidget(self)
        self.content_widget.setObjectName('content_widget')
        self.content_widget.setLayout(self.content_layout)
        self.content_widget.setStyleSheet('#content_widget{border: 1px dotted pink;}')
        self.layout.addWidget(self.content_widget)

    def get_user_widget(self, user, avatar_data):
        user_widget = UserWidget(user=user, avatar_data=avatar_data, parent=self)
        return user_widget

    def get_avatar(self, identifier, avatar=None):
        if identifier == 'def' or not avatar:
            url = 'https://cdn.discordapp.com/embed/avatars/3.png'
        else:
            url = 'https://cdn.discordapp.com/avatars/%s/%s.jpg' % (identifier, avatar)
        data = self.image_getter.from_url(url)
        return data

    def toggle(self):
        if self.is_visible:
            self.header_widget.hide()
            self.content_widget.setStyleSheet('#content_widget{border: none;}')
        else:
            self.header_widget.show()
            self.content_widget.setStyleSheet('#content_widget{border: 1px dotted pink;}')
        self.is_visible = not self.is_visible

    def you_left_voice_channel(self):
        self.clear_users()

    def clear_users(self):
        self.users = {}
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            self.content_layout.removeWidget(widget)
            if widget:
                widget.setParent(None)

    def someone_joined_channel(self, data):
        user = data['data']['user']
        user['nick'] = data['data']['nick']
        user['voice_state'] = data['data']['voice_state']

        if self.users.get(user['id']):
            return self.update_user(user)
        else:
            self.users[user['id']] = user
            user['avatar_data'] = self.get_avatar(user['id'], user['avatar'])
            user_widget = self.get_user_widget(self.users[user['id']], self.users[user['id']]['avatar_data'])
            self.content_layout.addWidget(user_widget)
            self.update_user(user)

    def someone_left_channel(self, data):
        user_id = data['data']['user']['id']
        if self.parent().discord_connector.user['id'] == user_id:
            self.clear_users()
            return

        del self.users[user_id]

        widget = self.find_user_widget(user_id)
        if not widget:
            return

        self.content_layout.removeWidget(widget)
        widget.setParent(None)

    def update_user(self, user):
        # TODO: WTF
        widget = self.find_user_widget(user['id'])

        if user['nick'] != widget.nick_label.text():
            widget.nick_label.setText(user['nick'])

        if user['voice_state']['deaf'] \
            or user['voice_state']['self_deaf'] \
            or ( \
                (user['voice_state']['deaf'] or user['voice_state']['self_deaf']) \
                and (user['voice_state']['mute'] or user['voice_state']['self_mute']) \
            ):

            if user.get('deafen'):
                return

            pixmap = QPixmap(':/images/deaf.png')
            for qlabel in widget.findChildren(QLabel):
                if qlabel.objectName() == 'mute_user':
                    qlabel.setParent(None)

            image = QLabel(widget, text='d')
            image.setObjectName('deaf_user')
            image.setPixmap(pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.FastTransformation))
            image.setFixedSize(20, 20)
            widget.layout().addWidget(image, 0, 1, Qt.AlignRight | Qt.AlignBottom)
            user['deafen'] = True
            return

        if user['voice_state']['mute'] or user['voice_state']['self_mute']:
            pixmap = QPixmap(':/images/mute.png')
            for qlabel in widget.findChildren(QLabel):
                if qlabel.objectName() == 'deaf_user':
                    qlabel.setParent(None)
            image = QLabel(widget, text='d')
            image.setObjectName('mute_user')
            image.setPixmap(pixmap.scaled(20, 20, Qt.KeepAspectRatio, Qt.FastTransformation))
            image.setFixedSize(20, 20)
            widget.layout().addWidget(image, 0, 1, Qt.AlignRight | Qt.AlignBottom)
            user['muted'] = True


        if not user['voice_state']['mute'] and not user['voice_state']['self_mute']:
            for qlabel in widget.findChildren(QLabel):
                if qlabel.objectName() == 'mute_user':
                    qlabel.setParent(None)
            user['mute'] = False

        if not user['voice_state']['deaf'] and not user['voice_state']['self_deaf']:
            for qlabel in widget.findChildren(QLabel):
                if qlabel.objectName() == 'deaf_user':
                    qlabel.setParent(None)
            user['deafen'] = False

    def you_joined_voice_channel_signal(self, data=None):
        self.clear_users()

    def speaking_start_signal(self, data):
        user_id = data['data']['user_id']
        self.set_user_widget_border(user_id, '2px solid green')

    def speaking_stop_signal(self, data):
        user_id = data['data']['user_id']
        self.set_user_widget_border(user_id, '0px')

    def set_user_widget_border(self, user_id, border):
        widget = self.find_user_widget(user_id)
        if not widget:
            return
        widget.setStyleSheet('#user_widget_%s { border: %s}' % (user_id, border))

    def find_user_widget(self, user_id):
        for widget in self.content_widget.findChildren(QWidget):
            if widget.objectName() == 'user_widget_%s' % user_id:
                return widget
        return None
