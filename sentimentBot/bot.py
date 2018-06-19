import re
import socket
import time
from threading import Thread
from twitchChatSentimentBot.settings import TWITCH_BOT_SETTINGS
from sentimentBot.signals import twitch_message


class TwitchBot(object):
    running_bot = False
    message_regex = re.compile(r':([a-zA-Z0-9_]+)!.+@.+ PRIVMSG (#[a-zA-Z0-9_]+) :([^\r]+)')
    pool_rate = 5

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
        self.join_channel(self.channel)

    def join_channel(self, channel):
        self.channel = channel
        self.socket.send("JOIN {}\r\n".format(channel).encode("utf-8"))
        response = ''
        while response.find('End of /NAMES list') == -1:
            response = self.socket.recv(1024).decode("utf-8")
            response = response.strip('\r\n')
        print("User: '%(user)s' has joined Channel '%(channel)s'" % {'user': self.username, 'channel': channel})

    def chat(self, message):
        self.socket.send("PRIVMSG {0} :{1}\r\n".format(self.channel, message).encode('utf-8'))

    def listen(self):
        while True:
            response = self.socket.recv(1024).decode("utf-8")
            # TODO PONG!
            twitch_message.send(
                sender=self.__class__,
                messages=[
                    {'user': x[0], 'channel': x[1], 'message': x[2]}
                    for x in self.message_regex.findall(response)],
            )
            time.sleep(self.pool_rate)

