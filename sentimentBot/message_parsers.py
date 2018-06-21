from django.dispatch import receiver
from sentimentBot.signals import twitch_message
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sentimentBot.models import TwitchEmote

logger = logging.getLogger('twitch')


class TwitchSentimentAnalyser(SentimentIntensityAnalyzer):
    instance = None

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance

    def make_lex_dict(self):
        # Update lexicon with twitch emotes
        lex = super().make_lex_dict()
        lex.update({x.word: x.positivity for x in TwitchEmote.objects.all()})
        return lex


@receiver(twitch_message)
def hype_meter(sender, messages, **kwargs):
    pass


@receiver(twitch_message)
def active_users(sender, messages, **kwargs):
    for message in messages:
        sender.users[message['user']] = sender.users.get(message['user'], 0) + 1


@receiver(twitch_message)
def sentiment_meter(sender, messages, **kwargs):
    sentiment_analyzer = TwitchSentimentAnalyser.get_instance()
    for message in messages:
        message.update(sentiment_analyzer.polarity_scores(message['message']))
        if message['compound'] != 0:
            print("[%(compound)s] %(user)s: %(message)s" % message)


@receiver(twitch_message)
def chat_log(sender, messages, **kwargs):
    for line in messages:
        logger.debug("%(channel)s: %(user)s: %(message)s" % line)
