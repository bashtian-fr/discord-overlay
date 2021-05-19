from PyQt5.QtCore import (
    QObject,
    pyqtSignal,
)


class DiscordConnectorCommunicator(QObject):
    # Define the signals:
    you_joined_voice_channel_signal = pyqtSignal()
    you_left_voice_channel_signal = pyqtSignal()

    someone_left_voice_channel_signal = pyqtSignal(dict)
    someone_joined_voice_channel_signal = pyqtSignal(dict)

    update_voice_channel_signal = pyqtSignal(str)

    speaking_start_signal = pyqtSignal(dict)
    speaking_stop_signal = pyqtSignal(dict)

    authenticated = pyqtSignal()

    connection_error = pyqtSignal(str)
