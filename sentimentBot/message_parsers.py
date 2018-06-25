from django.dispatch import receiver
from sentimentBot.signals import twitch_message
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sentimentBot.models import TwitchEmote
from numpy import mean
from twitchChatSentimentBot.settings import TWITCH_LEXICON

logger = logging.getLogger('twitch')


class TwitchSentimentAnalyser(SentimentIntensityAnalyzer):
    instance = None
    sentiment_value = 0
    min_cap, max_cap = -25, 25

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance

    def make_lex_dict(self):
        # Update lexicon with twitch emotes
        lex = super().make_lex_dict()
        lex.update({x.word: x.positivity for x in TwitchEmote.objects.all()})
        lex.update(TWITCH_LEXICON)
        return lex

    @classmethod
    def update_sentiment(cls, value):
        cls.sentiment_value += value
        cls.sentiment_value = max(cls.sentiment_value, cls.min_cap)
        cls.sentiment_value = min(cls.sentiment_value, cls.max_cap)

    @property
    def sentiment(self):
        value = self.sentiment_value
        return 'Positive' if value > 2.5 else 'Negative' if value < -2.5 else 'Neutral'

    def __str__(self):
        return "%(value).2f%% %(sentiment)s" % {'value': self.sentiment_value * 4, 'sentiment': self.sentiment}


class TwitchHypeTracker(object):
    """Tracks hype by number of messages received minus the average number of messages over a period of time"""
    instance = None
    hype_level = 0
    min_hype, max_hype = 0, 100
    hype_log = [0] * 10
    hype_emojis = {
        0: '_(._.)_',
        10: 'ヽ(´ー｀)ﾉ',
        25: '( ﾟヮﾟ)',
        50: '(＾◇＾)',
        65: '(*´▽｀*)(*°∀°)=3',
        80: '( ﾟдﾟ) (/◕ヮ◕)/ Σ(ﾟДﾟ)',
        90: '(╯°□°）╯︵ ┻━┻︵ヽ(`Д´)ﾉ︵ ┻━┻ (ノಠ益ಠ)ノ彡┻━┻'
    }

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance

    @property
    def hype_string(self):
        emoji_key = 0
        for key in sorted(self.hype_emojis.keys(), reverse=True):
            if self.hype_level >= key:
                emoji_key = key
                break

        return self.hype_emojis.get(emoji_key, '')

    def _modify_hype(self, hype):
        self.hype_level += (hype * 2)  # x2 mult for more significant hype swings
        self.hype_level = min(self.hype_level, self.max_hype)
        self.hype_level = max(self.hype_level, self.min_hype)

    def update_hype(self, hype_level):
        # Hype is current number of messages sent minus the average messages over the last period
        average = mean(self.hype_log)

        self.hype_log.pop(len(self.hype_log) - 1)
        self.hype_log.insert(0, hype_level)
        self._modify_hype(hype_level - average)

    def __str__(self):
        return "hype: %(hype_level).2f%% %(hype)s" % {'hype_level': self.hype_level, 'hype': self.hype_string}


@receiver(twitch_message)
def hype_meter(sender, messages, **kwargs):
    hype_tracker = TwitchHypeTracker.get_instance()
    hype_tracker.update_hype(len(messages))
    print(hype_tracker)


@receiver(twitch_message)
def sentiment_meter(sender, messages, **kwargs):
    sentiment_analyzer = TwitchSentimentAnalyser.get_instance()
    for message in messages:
        message.update(sentiment_analyzer.polarity_scores(message['message']))
        if message['compound'] != 0:
            sentiment_analyzer.update_sentiment(message['compound'])
    print(sentiment_analyzer)


@receiver(twitch_message)
def chat_log(sender, messages, **kwargs):
    for line in messages:
        logger.debug("%(channel)s: [%(compound)s] %(user)s: %(message)s" % line)
