from django.db import models


class TwitchChannel(models.Model):
    name = models.CharField(max_length=32)


class TwitchChatWordPositivity(models.Model):
    # Positivity is used in vader SentimentAnalysis indicating positivity of word
    # Ranges from -3 (very negative) to +3 (very positive)
    positivity = models.FloatField()
    word = models.CharField(max_length=32)


class TwitchEmote(TwitchChatWordPositivity):
    channel = models.ForeignKey(TwitchChannel, null=True)
