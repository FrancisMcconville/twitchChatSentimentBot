import re
import socket
import time
from threading import Thread
from twitchChatSentimentBot.settings import TWITCH_BOT_SETTINGS


class TwitchBot(object):
    running_bot = False

    def __init__(self, username, oauth, channel=None, **kwargs):
        super().__init__()
        self.channel = channel or '#%s' % username
        self.username = username
        self.oauth = oauth
        self.socket = socket.socket()

    def start(self):
        if not self.__class__.running_bot:
            self._connect()
            self.__class__.running_bot = Thread(target=self.listen, daemon=True)
            self.__class__.running_bot.start()

    def _connect(self):
        self.socket.connect((TWITCH_BOT_SETTINGS['host'], TWITCH_BOT_SETTINGS['port']))
        self.socket.send("PASS {}\r\n".format(self.oauth).encode("utf-8"))
        self.socket.send("NICK {}\r\n".format(self.username).encode("utf-8"))
        self.socket.send("JOIN {}\r\n".format(self.channel).encode("utf-8"))

    def join_channel(self, channel):
        self.channel = channel
        self.socket.send("JOIN #{}\r\n".format(TWITCH_BOT_SETTINGS['username']).encode("utf-8"))

    def chat(self, message):
        self.socket.send("PRIVMSG {0} :{1}\r\n".format(self.channel, message).encode('utf-8'))

    def listen(self):
        while True:
            response = self.socket.recv(1024).decode("utf-8")
            if response == "PING: tmi.twitch.tv":
                self.socket.send("PONG: tmi.twitch.tv\r\n".encode('utf-8'))
            else:
                print(response)
                # TODO if valid chat message, fire off a signal for that chat message to be parsed
            time.sleep(1)
