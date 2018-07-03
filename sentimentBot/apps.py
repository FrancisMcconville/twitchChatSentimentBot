from django.apps import AppConfig


class SentimentbotConfig(AppConfig):
    name = 'sentimentBot'
    verbose_name = "Sentiment Bot"

    def ready(self):
        import sentimentBot.twitch_message_listeners
