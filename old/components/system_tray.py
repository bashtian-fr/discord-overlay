from PyQt5.QtWidgets import (
    QLabel,
    QSystemTrayIcon,
    QMenu,
    QAction,
    QDialog,
    qApp,
    QGridLayout,
    QCheckBox,
    QGroupBox,
    QVBoxLayout,
    QComboBox,
    QSpinBox,
)
from do import APPLICATION_NAME
from do.libs.helpers import get_app_settings, load_qss_for


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)
        self.setToolTip(APPLICATION_NAME)
        self.init_ui()

    def init_ui(self):
        self.settings_window = SystemTrayIconSettingsDialog(parent=self.parent())
        self.settings_window.hide()
        self._menu = QMenu()

        toggle_overlay_action = QAction(
            '&Toggle the overlay',
            parent=self,
            triggered=self.toggle_overlay
        )

        settings_action = QAction('&Settings', parent=self, triggered=self.show_settings_window)
        # settings_menu = self._menu.addMenu('&Settings')
        # show_only_speakers = QAction(
        #     '&Only Speakers',
        #     parent=self,
        #     triggered=self.show_only_speakers_callback,
        #     checkable=True,
        #     checked = get_app_settings().value('show_only_speakers', defaultValue=False, type=bool)
        # )
        # settings_menu.addAction(show_only_speakers)

        quit_action = QAction('&Exit', parent=self, triggered=self.exit)
        self._menu.addAction(toggle_overlay_action)
        self._menu.addAction(settings_action)
        self._menu.addAction(quit_action)

        self.setContextMenu(self._menu)
        self.show()

    def show_settings_window(self):
        self.settings_window.show()


    def toggle_overlay(self):
        self.parent().discord_overlay.toggle()

    def exit(self):
        qApp.quit()


class SystemTrayIconSettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setObjectName('SystemTrayIconSettingsDialog')
        self.setStyleSheet(load_qss_for('SystemTrayIconSettingsDialog'))
        self.setWindowTitle('Settings')
        self.setMinimumWidth(200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        group_box = QGroupBox('General Options', parent=self)
        layout.addWidget(group_box)
        self.setLayout(layout)

        # option 1
        only_speakers_checkbox = QCheckBox(text='Only Speakers', parent=self)
        only_speakers_checkbox.setChecked(get_app_settings().value('show_only_speakers', defaultValue=False, type=bool))
        only_speakers_checkbox.stateChanged.connect(self.show_only_speakers_callback)

        # option 2
        speaker_border_color_combobox = QComboBox(parent=group_box)
        speaker_border_color_combobox.addItems(['green', 'red', 'yellow', 'purple', 'blue'])
        speaker_border_color_combobox.setCurrentText(get_app_settings().value('speaker_border_color', defaultValue='green', type=str))
        speaker_border_color_combobox.currentTextChanged.connect(self.speaker_border_color_combobox_callback)

        # option 3
        speaker_border_color_size = QSpinBox(parent=group_box)
        speaker_border_color_size.setRange(1, 5)
        speaker_border_color_size.setValue(get_app_settings().value('speaker_border_color_size', defaultValue=1, type=int))
        speaker_border_color_size.valueChanged.connect(self.speaker_border_color_size_callback)

        # option 2
        user_avatar_shape_combobox = QComboBox(parent=group_box)
        user_avatar_shape_combobox.addItems(['square', 'round'])
        user_avatar_shape_combobox.setCurrentText(get_app_settings().value('user_avatar_shape', defaultValue='square', type=str))
        user_avatar_shape_combobox.currentTextChanged.connect(self.user_avatar_shape_combobox_callback)

        #
        group_box_layout = QGridLayout()
        group_box_layout.addWidget(only_speakers_checkbox, 0, 0)
        group_box_layout.addWidget(speaker_border_color_combobox, 1, 0)
        group_box_layout.addWidget(speaker_border_color_size, 2, 0)
        group_box_layout.addWidget(user_avatar_shape_combobox, 3, 0)
        group_box.setLayout(group_box_layout)

    def show_only_speakers_callback(self, checked):
        get_app_settings().setValue('show_only_speakers', checked)
        dicord_overlay = self.parent().discord_overlay
        if checked:
            dicord_overlay.hide_all_users()
        else:
            dicord_overlay.show_all_users()

    def speaker_border_color_combobox_callback(self, text):
        get_app_settings().setValue('speaker_border_color', text)

    def speaker_border_color_size_callback(self, value):
        get_app_settings().setValue('speaker_border_color_size', value)

    def user_avatar_shape_combobox_callback(self, text):
        get_app_settings().setValue('user_avatar_shape', text)
