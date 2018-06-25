from django.apps import AppConfig
import sys
from sentimentBot.bot import TwitchBot
from twitchChatSentimentBot.settings import TWITCH_BOT_SETTINGS


class SentimentbotConfig(AppConfig):
    name = 'sentimentBot'
    verbose_name = "Sentiment Bot"

    def ready(self):
        import sentimentBot.message_parsers
        if 'runserver' not in sys.argv:
            return True
        bot = TwitchBot(**TWITCH_BOT_SETTINGS)
        bot.start()
