from django.apps import AppConfig
import sys
from sentimentBot.bot import TwitchBot
from twitchChatSentimentBot.settings import TWITCH_BOT_SETTINGS


class SentimentbotConfig(AppConfig):
    name = 'sentimentBot'
    verbose_name = "Sentiment Bot"

    def ready(self):
        from sentimentBot.message_parsers import sentiment_meter, hype_meter, active_users
        if 'runserver' not in sys.argv:
            return True
        bot = TwitchBot(**TWITCH_BOT_SETTINGS)
        bot.start()
