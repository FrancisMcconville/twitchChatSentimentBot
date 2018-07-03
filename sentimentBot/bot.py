import re
import socket
import time
from sentimentBot.signals import twitch_message
from threading import Thread
from twitchChatSentimentBot.utils.patterns import Borg
from twitchChatSentimentBot.settings import TWITCH_BOT_SETTINGS


class TwitchBot(Borg):
    _message_regex = re.compile(r':([a-zA-Z0-9_]+)!.+@.+ PRIVMSG (#[a-zA-Z0-9_]+) :([^\r]+)')
    _ping_regex = re.compile(r"PING :tmi\.twitch\.tv")
    poll_rate = 2
    users = {}

    def __init__(self):
        super().__init__()
        self.__dict__.update(TWITCH_BOT_SETTINGS)
        if not hasattr(self, 'listen_thread'):
            self.socket = socket.socket()
            self._connect()
            self.listen_thread = Thread(target=self._listen, daemon=True)
            self.listen_thread.start()

    def _connect(self):
        self.socket.connect((TWITCH_BOT_SETTINGS['host'], TWITCH_BOT_SETTINGS['port']))
        self.socket.send("PASS {}\r\n".format(self.oauth).encode("utf-8"))
        self.socket.send("NICK {}\r\n".format(self.username).encode("utf-8"))
        self.join_channel(self.channel)

    def _send_pong(self):
        self.socket.send(bytes("PONG\n", encoding="utf-8"))

    def _listen(self):
        while True:
            try:
                response = self.socket.recv(1024).decode("utf-8")
            except (UnicodeDecodeError, BlockingIOError):
                response = ''

            if self._ping_regex.match(response):
                self._send_pong()

            twitch_message.send(
                sender=self,
                messages=[
                    {'user': x[0], 'channel': x[1], 'message': x[2]} for x in self._message_regex.findall(response)
                ],
            )
            time.sleep(self.poll_rate)

    def join_channel(self, channel):
        self.socket.setblocking(True)
        self.channel = channel
        self.socket.send("JOIN {}\r\n".format(channel).encode("utf-8"))
        response = ''
        while response.find('End of /NAMES list') == -1:
            response = self.socket.recv(1024).decode("utf-8")
            response = response.strip('\r\n')
        self.socket.setblocking(False)
        print("User: '%(user)s' has joined Channel '%(channel)s'" % {'user': self.username, 'channel': channel})

    def chat(self, message):
        self.socket.send("PRIVMSG {0} :{1}\r\n".format(self.channel, message).encode('utf-8'))



