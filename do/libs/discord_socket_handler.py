import json
import requests
from websocket import create_connection


'''
Part of the connector is based on the one of Trigg's:
https://github.com/trigg/Discover/blob/master/discover_overlay/discord_connector.py
'''


class DiscordSocketHandler:

    def __init__(self, client_id, origin, address, port):
        self.client_id = client_id
        self.origin = origin
        self.address = address
        self.port = port
        self.websocket = None
        self.access_token = None

    def connect(self):
        if self.websocket:
            return

        self.websocket = create_connection(
            'ws://{address}:{port}/?v=1&client_id={client_id}'.format(
                address=self.address,
                port=self.port,
                client_id=self.client_id
            ),
            origin=self.origin,
        )

    def sub_raw(self, event, args, nonce):
        cmd = {
            'cmd': 'SUBSCRIBE',
            'args': args,
            'evt': event,
            'nonce': nonce
        }
        self.websocket.send(json.dumps(cmd))

    def unsub_raw(self, event, args, nonce):
        cmd = {
            'cmd': 'UNSUBSCRIBE',
            'args': args,
            'evt': event,
            'nonce': nonce
        }
        self.websocket.send(json.dumps(cmd))

    def sub_server(self):
        self.sub_raw('VOICE_CHANNEL_SELECT', {}, 'VOICE_CHANNEL_SELECT')
        self.sub_raw('VOICE_CONNECTION_STATUS', {}, 'VOICE_CONNECTION_STATUS')

    def sub_channel(self, event, channel_id):
        self.sub_raw(event, {'channel_id': channel_id}, channel_id)

    def unsub_channel(self, event, channel_id):
        self.unsub_raw(event, {'channel_id': channel_id}, channel_id)

    def unsub_voice_channel(self, channel_id):
        self.unsub_channel('VOICE_STATE_CREATE', channel_id)
        self.unsub_channel('VOICE_STATE_UPDATE', channel_id)
        self.unsub_channel('VOICE_STATE_DELETE', channel_id)
        self.unsub_channel('SPEAKING_START', channel_id)
        self.unsub_channel('SPEAKING_STOP', channel_id)

    def sub_voice_channel(self, channel_id):
        self.sub_channel('VOICE_STATE_CREATE', channel_id)
        self.sub_channel('VOICE_STATE_UPDATE', channel_id)
        self.sub_channel('VOICE_STATE_DELETE', channel_id)
        self.sub_channel('SPEAKING_START', channel_id)
        self.sub_channel('SPEAKING_STOP', channel_id)

    def get_access_token_stage1(self):
        cmd = {
            'cmd': 'AUTHORIZE',
            'args':
            {
                'client_id': self.client_id,
                'scopes': ['rpc', 'messages.read'],
                'prompt': 'none',
            },
            'nonce': 'deadbeef'
        }
        self.websocket.send(json.dumps(cmd))

    def get_access_token_stage2(self, code1):
        url = 'https://streamkit.discord.com/overlay/token'
        myobj = {'code': code1}
        response = requests.post(url, json=myobj)
        try:
            jsonresponse = json.loads(response.text)
        except json.JSONDecodeError:
            jsonresponse = {}

        if 'access_token' in jsonresponse:
            self.access_token = jsonresponse['access_token']
            self.request_authentication_token()
        else:
            sys.exit(1)

    def request_authentication_token(self):
        cmd = {
            "cmd": "AUTHENTICATE",
            "args": {
                "access_token": self.access_token
            },
            "nonce": "deadbeef"
        }
        self.websocket.send(json.dumps(cmd))

    def request_find_user(self):
        cmd = {
            'cmd': 'GET_SELECTED_VOICE_CHANNEL',
            'args': {},
            'nonce': 'deadbeef'
        }
        self.websocket.send(json.dumps(cmd))

    def request_channel_details(self, channel_id):
        cmd = {
            'cmd': 'GET_CHANNEL',
            'args': {
                'channel_id': channel_id
            },
            'nonce': channel_id
        }
        self.websocket.send(json.dumps(cmd))
