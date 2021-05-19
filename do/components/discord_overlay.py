from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
)
from do import APPLICATION_NAME
from do.components.overlay import Overlay
from do.components.overlay_header import OverlayHeaderWidget
from do.components.user_widget import UserWidget, load_qss_for
from do.libs.helpers import (
    get_url_data,
    get_app_settings,
)


class DiscordOverlay(Overlay):
    def __init__(self, parent):
        super().__init__(name=APPLICATION_NAME, pos_x=0, pos_y=0, width=200, height=200, parent=parent)
        self.setAttribute(Qt.WA_AlwaysShowToolTips)
        self.avatars = {}
        self.default_avatar = self.get_avatar('default')
        self.header_widget = None
        self.is_visible = True
        self.old_pos = self.pos()
        self.user_container = None
        self.users = {}
        self.init_ui()

    def init_ui(self):
        self.header_widget = OverlayHeaderWidget(parent=self, title=self.name)
        self.scroll_area = DiscordOverlayScrollArea(parent=self)
        self.layout.addWidget(self.header_widget)
        self.layout.addWidget(self.scroll_area)
        self.header_widget.show()

    def get_user_widget(self, user, avatar_data):
        user_widget = UserWidget(user=user, avatar_data=avatar_data, parent=self)
        return user_widget

    def get_avatar(self, identifier, avatar=None):
        if identifier == 'default' or not avatar:
            url = 'https://cdn.discordapp.com/embed/avatars/3.png'
        else:
            url = f'https://cdn.discordapp.com/avatars/{identifier}/{avatar}.jpg'
        data = get_url_data(url)
        return data

    def toggle(self):
        if self.is_visible:
            self.header_widget.hide()
            self.scroll_area.setStyleSheet('background: transparent; border: none;')
            self.parent().sys_tray_icon.showMessage(
                APPLICATION_NAME,
                f'The {APPLICATION_NAME} is running in background'
            )
        else:
            self.header_widget.show()
            self.scroll_area.setStyleSheet('background: transparent; border: 1px dotted pink;')
        self.is_visible = not self.is_visible

    def you_left_voice_channel(self):
        self.clear_users()

    def clear_users(self):
        self.users = {}
        for i in reversed(range(self.scroll_area.user_container.layout().count())):
            widget = self.scroll_area.user_container.layout().itemAt(i).widget()
            self.scroll_area.user_container.layout().removeWidget(widget)
            if widget:
                widget.setParent(None)

    def someone_joined_channel(self, data):
        user = data['data']['user']
        user['nick'] = data['data']['nick']
        user['voice_state'] = data['data']['voice_state']

        if self.users.get(user['id']):
            # he once joined
            self.update_user(user)
        else:
            self.add_user(user)

    def add_user(self, user):
        self.users[user['id']] = user
        user['avatar_data'] = self.get_avatar(user['id'], user['avatar'])
        user_widget = self.get_user_widget(self.users[user['id']], self.users[user['id']]['avatar_data'])

        if get_app_settings().value('show_only_speakers', defaultValue=False, type=bool):
            user_widget.hide()

        self.scroll_area.user_container.layout().addWidget(user_widget)
        self.update_user(user)

    def someone_left_channel(self, data):
        user_id = data['data']['user']['id']
        if self.parent().discord_connector.user['id'] == user_id:
            # clean if main user leaves
            return self.clear_users()
        self.remove_user(user_id)

    def remove_user(self, user_id):
        del self.users[user_id]
        widget = self.find_user_widget(user_id)
        if not widget:
            return
        self.scroll_area.user_container.layout().removeWidget(widget)
        widget.setParent(None)

    def is_user_deafen(self, user):
        if user['voice_state']['deaf'] \
            or user['voice_state']['self_deaf'] \
                and (
                    user['voice_state']['mute'] \
                    or user['voice_state']['self_mute']
                ):
            return True

        if user['voice_state']['deaf'] \
            or user['voice_state']['self_deaf']:
            return True

        return False

    def is_user_mute(self, user):
        if user['voice_state']['mute'] \
            or user['voice_state']['self_mute']:
            return True

        return False

    def update_user(self, user):
        user_widget = self.find_user_widget(user['id'])

        if user['nick'] != user_widget.nick_label.text():
            user_widget.update_nickname(user['nick'])

        if self.is_user_deafen(user) \
            and not user.get('deafened'):
            user_widget.remove_mute_icon()
            user_widget.add_deaf_icon()
            user['deafened'] = True

        if self.is_user_mute(user) \
            and not user.get('muted') \
                and not user.get('deafened'):
            user_widget.remove_deaf_icon()
            user_widget.add_mute_icon()
            user['muted'] = True

        if not self.is_user_mute(user):
            user_widget.remove_mute_icon()
            user['muted'] = False

        if not self.is_user_deafen(user):
            user_widget.remove_deaf_icon()
            user['deafened'] = False

    def you_joined_voice_channel_signal(self):
        # We clear the overlay when we join a chan
        self.clear_users()

    def speaking_start_signal(self, data):
        user_id = data['data']['user_id']
        self.show_user(user_id)
        self.set_user_speaking(user_id)

    def speaking_stop_signal(self, data):
        user_id = data['data']['user_id']
        if get_app_settings().value('show_only_speakers', defaultValue=False, type=bool):
            self.hide_user(user_id)
        self.set_user_not_speaking(user_id)

    def set_user_not_speaking(self, user_id):
        widget = self.find_user_widget(user_id)
        if widget:
            widget.stop_speaking()

    def set_user_speaking(self, user_id):
        widget = self.find_user_widget(user_id)
        if widget:
            widget.start_speaking()

    def show_user(self, user_id):
        widget = self.find_user_widget(user_id)
        if widget:
            widget.show()

    def hide_user(self, user_id):
        widget = self.find_user_widget(user_id)
        if widget:
            widget.hide()

    def find_user_widget(self, user_id):
        for widget in self.scroll_area.user_container.findChildren(QWidget):
            if widget.objectName() == f'user_widget_{user_id}' :
                return widget
        return None

    def show_or_hide_all_users(self, show=False):
        for user_widget in self.scroll_area.user_container.findChildren(QWidget):
            if 'user_widget' in user_widget.objectName() and not user_widget.speaking:
                if show:
                    user_widget.show()
                else:
                    user_widget.hide()

    def hide_all_users(self):
        self.show_or_hide_all_users(show=False)

    def show_all_users(self):
        self.show_or_hide_all_users(show=True)


class DiscordOverlayUserContainer(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setObjectName('DiscordOverlayUserContainer')
        self.setStyleSheet(load_qss_for('DiscordOverlayUserContainer'))
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setDirection(QVBoxLayout.BottomToTop)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)


class DiscordOverlayScrollArea(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setObjectName('DiscordOverlayScrollArea')
        self.setStyleSheet(load_qss_for('DiscordOverlayScrollArea'))
        self.setWidgetResizable(True)
        self.init_ui()

    def init_ui(self):
        self.user_container = DiscordOverlayUserContainer(self)
        self.setWidget(self.user_container)
