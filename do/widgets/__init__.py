from PyQt5.QtCore import QPoint, QSize, Qt
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDesktopWidget,
    QDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QShortcut,
    QSpinBox,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QSizeGrip,
    QScrollArea,
)
from PyQt5.QtGui import (
    QIcon,
    QPixmap,
)

from ..libs.helpers import get_app_settings, load_qss_for


class CentralWidget(QFrame):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setAttribute(Qt.WA_AlwaysShowToolTips)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)


class CentralWidgetScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(load_qss_for(self.__class__.__name__))
        self.setWidgetResizable(True)

    def hide_border(self):
        self.setStyleSheet('background: transparent; border: none;')

    def show_border(self):
        self.setStyleSheet('background: transparent; border: 1px dotted gray;')


class CentralWidgetScrollAreaHeaderWidget(QWidget):
    def __init__(self, tooltip, main_window, parent):
        super().__init__(parent=parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(load_qss_for(self.__class__.__name__))
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(Qt.OpenHandCursor)
        self.setToolTip(tooltip)
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        sp_retain = self.sizePolicy()
        sp_retain.setRetainSizeWhenHidden(True)
        self.setSizePolicy(sp_retain)

    def mousePressEvent(self, event): # pylint: disable=invalid-name
        self.main_window.old_pos = event.globalPos()
        self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event): # pylint: disable=unused-argument,invalid-name
        self.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event): # pylint: disable=invalid-name
        delta = QPoint(event.globalPos() - self.main_window.old_pos)
        pos_x = self.main_window.x() + delta.x()
        pos_y = self.main_window.y() + delta.y()
        self.main_window.move(pos_x, pos_y)
        self.main_window.old_pos = event.globalPos()


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
        self.setCursor(Qt.PointingHandCursor)

    def mouseMoveEvent(self, event): # pylint: disable=invalid-name,unused-argument
        # implement mouseMoveEvent to override parent one
        # in order to avoid setting position when clicking button
        pass


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(load_qss_for(self.__class__.__name__))
        self.setWindowTitle('Settings')
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowStaysOnTopHint
        )
        self.setMinimumWidth(200)
        self.setWindowIcon(QIcon(':/images/icon.ico'))
        self.old_pos = self.pos()
        self.init_ui()
        self.center()
        QShortcut('Ctrl+w', self).activated.connect(self.hide)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        #Header
        header_widget = SettingsDialogHeader(parent=self)

        layout.addWidget(header_widget)
        #Content
        content_widget = QWidget(parent=self)
        content_widget_layout = QVBoxLayout()
        content_widget.setLayout(content_widget_layout)
        layout.addWidget(content_widget)

        #Content data
        group_box = QGroupBox('General Options', parent=content_widget)
        content_widget_layout.addWidget(group_box)

        # option 1
        only_speakers_checkbox = QCheckBox(text='Only Speakers', parent=content_widget)
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
        # TODO:

        # dicord_overlay = self.parent().discord_overlay
        # if checked:
        #     dicord_overlay.hide_all_users()
        # else:
        #     dicord_overlay.show_all_users()

    def speaker_border_color_combobox_callback(self, text):
        get_app_settings().setValue('speaker_border_color', text)

    def speaker_border_color_size_callback(self, value):
        get_app_settings().setValue('speaker_border_color_size', value)

    def user_avatar_shape_combobox_callback(self, text):
        get_app_settings().setValue('user_avatar_shape', text)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        qp = QPoint(qr.topLeft().x() - qr.height()/2, qr.topLeft().y() - qr.width()/2)
        self.move(qp)


class SettingsDialogHeader(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(load_qss_for(self.__class__.__name__))
        self.setFixedHeight(22)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(layout)

        icon = QLabel()
        icon.setPixmap(QIcon(':/images/icon.ico').pixmap(16,16))
        layout.addWidget(icon)

        title = QLabel(f'{QApplication.instance().applicationName()} - Settings')
        layout.addWidget(title, 1, Qt.AlignLeft)

        close = SettingsDialogHeaderCloseButton(parent=self)
        layout.addWidget(close, 1, Qt.AlignRight)

    def mousePressEvent(self, event): # pylint: disable=invalid-name
        self.parent().old_pos = event.globalPos()
    #     self.setCursor(Qt.ClosedHandCursor)

    # def mouseReleaseEvent(self, event): # pylint: disable=unused-argument,invalid-name
    #     self.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event): # pylint: disable=invalid-name
        delta = QPoint(event.globalPos() - self.parent().old_pos)
        pos_x = self.parent().x() + delta.x()
        pos_y = self.parent().y() + delta.y()
        self.parent().move(pos_x, pos_y)
        self.parent().old_pos = event.globalPos()


class SettingsDialogHeaderCloseButton(QToolButton):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setObjectName('SettingsDialogHeaderCloseButton')
        self.setContentsMargins(0, 0, 0, 0)
        #self.setIcon(QIcon(QPixmap(':/images/close.png')))
        #self.setMinimumSize(25, 16)
        #self.setIconSize(QSize(25, 16))
        self.clicked.connect(self.parent().parent().hide)

    def mouseMoveEvent(self, event):
        pass
