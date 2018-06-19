from django.apps import AppConfig
import sys
from sentimentBot.bot import TwitchBot
from sentimentBot.signals import twitch_message
from sentimentBot.message_parsers import hype_meter, sentiment_meter, unique_users
from twitchChatSentimentBot.settings import TWITCH_BOT_SETTINGS


class SentimentbotConfig(AppConfig):
    name = 'sentimentBot'
    verbose_name = "Sentiment Bot"

    def ready(self):
        if 'runserver' not in sys.argv:
            return True

        twitch_message.connect(hype_meter, TwitchBot)
        twitch_message.connect(sentiment_meter, TwitchBot)
        twitch_message.connect(unique_users, TwitchBot)

        bot = TwitchBot(**TWITCH_BOT_SETTINGS)
        bot.start()
