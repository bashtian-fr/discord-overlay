import json
import logging
import select
import time
from websocket import WebSocketConnectionClosedException
from do.libs.discord_connector_communicator import DiscordConnectorCommunicator
from do.libs.discord_socket_handler import DiscordSocketHandler


'''
Part of the connector is based on the one of Trigg's:
https://github.com/trigg/Discover/blob/master/discover_overlay/discord_connector.py
'''


VOICE_CHANNEL_TYPE = 2


class DiscordConnector:
    def __init__(self, client_id, discord_overlay, origin='https://streamkit.discord.com', socket_address='127.0.0.1', socket_port='6463'):
        self.comm = DiscordConnectorCommunicator()
        self.socket_handler = DiscordSocketHandler(client_id, origin, socket_address, socket_port)
        self.user = None
        self.current_voice_channel_id = None
        self.guilds = {}
        self.channels = {}
        self.userlist = {}
        self.last_connection = None
        self.authenticated = False
        self.supported_commands = [
            'DISPATCH',
            'AUTHENTICATE',
            'AUTHORIZE',
            'GET_GUILDS',
            'GET_CHANNELS',
            'GET_CHANNEL',
            'SUBSCRIBE',
            'UNSUBSCRIBE',
            'GET_SELECTED_VOICE_CHANNEL',
        ]
        self.supported_events = [
            'READY',
            'VOICE_STATE_UPDATE',
            'VOICE_CONNECTION_STATUS',
            'VOICE_CHANNEL_SELECT',
            'SPEAKING_START',
            'SPEAKING_STOP',
            'VOICE_STATE_CREATE',
            'VOICE_STATE_DELETE',
        ]

    def connect(self):
        try:
            self.socket_handler.connect()
        except ConnectionError as error:
            logging.error('ConnectionError: %s', error)
            self.comm.connection_error.emit('%s' % error)
            time.sleep(5)
        except ConnectionResetError as errpr:
            logging.error('ConnectionResetError: %s', error)
            self.comm.connection_error.emit('%s' % error)
            time.sleep(5)

    def handle(self):
        self.connect()
        ready_to_read, ready_to_write, in_error = select.select((self.socket_handler.websocket.sock,), (), (), 0)
        while ready_to_read:
            try:
                msg = self.socket_handler.websocket.recv()
                self.on_message(msg)
                ready_to_read, ready_to_write, in_error = select.select((self.socket_handler.websocket.sock,), (), (), 0)
            except WebSocketConnectionClosedException as e:
                logging.error('While handling: %s' % e)
                self.on_close()
                return True
            except Exception as e:
                return self.comm.connection_error.emit('%s' % e)
        return True

    def on_close(self):
        logging.info('Connection closed')
        self.socket_handler.websocket = None

    def on_message(self, message):
        resp = json.loads(message)
        command = resp['cmd']
        logging.debug('Incoming command: %s' % command)

        if command not in self.supported_commands:
            logging.warn('Unsupported command: %s', command)
            return

        if command == 'DISPATCH':
            event = resp['evt']
            logging.debug('Incoming event: %s' % event)
            if event not in self.supported_events:
                logging.warn('Unsupported event: %s', event)
                return

            if event == 'READY':
                self.socket_handler.request_authentication_token()
                return

            if event == 'VOICE_STATE_CREATE':
                # When a user joins a subscribed voice channel
                self.comm.someone_joined_voice_channel_signal.emit(resp)
                return

            if event == 'VOICE_STATE_DELETE':
                # When a user parts a subscribed voice channel
                self.comm.someone_left_voice_channel_signal.emit(resp)
                if resp['data']['user']['id'] == self.user['id']:
                    self.current_voice_channel_id = None
                    self.comm.you_left_voice_channel_signal.emit()
                return

            if event == 'VOICE_STATE_UPDATE':
                # When a user's voice state changes in a subscribed voice channel (mute, volume, etc.)
                # when joining a chan, we get all user one by one
                self.comm.someone_joined_voice_channel_signal.emit(resp)
                return

            if event == 'VOICE_CHANNEL_SELECT':
                # We join or leave a channal
                # We need to unsubscribe from previous channel.

                channel_id = resp['data']['channel_id']
                if not channel_id:
                    self.socket_handler.unsub_voice_channel(self.current_voice_channel_id)
                    self.comm.you_left_voice_channel_signal.emit()
                    self.current_voice_channel_id = None
                    return

                self.set_active_channel(channel_id, True)
                return

            if event == 'VOICE_CONNECTION_STATUS':
                # When the client's voice connection status changes
                self.last_connection = resp['data']['state']
                return

            if event == 'SPEAKING_START':
                self.comm.speaking_start_signal.emit(resp)
                return

            if event == 'SPEAKING_STOP':
                self.comm.speaking_stop_signal.emit(resp)

            return

        if command == 'AUTHENTICATE':
            event = resp['evt']
            if event == 'ERROR':
                logging.info('Authenticating...')
                self.socket_handler.get_access_token_stage1()
                return
            else:
                self.user = resp['data']['user']
                logging.info('Authenticated as %s (%s)', self.user['username'], self.user['id'])
                self.authenticated = True
                self.comm.authenticated.emit()
                self.socket_handler.sub_server()
                self.socket_handler.request_find_user()
                return

        if command == 'AUTHORIZE':
            code = resp['data']['code']
            self.socket_handler.get_access_token_stage2(code)
            return

        if command in ['GET_CHANNEL', 'GET_SELECTED_VOICE_CHANNEL']:
            if resp['evt'] == 'ERROR':
                logging.info('Could not get room')
                return

            if command == 'GET_SELECTED_VOICE_CHANNEL':
                if not resp['data']:
                    return

            if resp['data']['type'] == VOICE_CHANNEL_TYPE:
                for voice in resp['data']['voice_states']:
                    if voice['user']['id'] == self.user['id']:
                        self.set_active_channel(resp['data']['id'])
                        break
            return

    def set_active_channel(self, channel_id, need_request=True):
        if not channel_id:
            self.comm.you_left_voice_channel_signal.emit()
            self.current_voice_channel_id = None
            self.socket_handler.unsub_voice_channel(channel_id)
            return

        if channel_id != self.current_voice_channel_id:
            self.comm.you_joined_voice_channel_signal.emit(channel_id)
            if self.current_voice_channel_id:
                self.socket_handler.unsub_voice_channel(self.current_voice_channel_id)
            self.socket_handler.sub_voice_channel(channel_id)
            self.current_voice_channel_id = channel_id

            if need_request:
                self.socket_handler.request_channel_details(channel_id)

    def set_in_room(self, userid, present):
        if present:
            if userid not in self.in_room:
                self.in_room.append(userid)
        else:
            if userid in self.in_room:
                self.in_room.remove(userid)
