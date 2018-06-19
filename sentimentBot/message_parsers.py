from django.dispatch import receiver
from sentimentBot.signals import twitch_message
from sentimentBot.bot import TwitchBot


@receiver(twitch_message, sender=TwitchBot)
def hype_meter(sender, user, channel, message, **kwargs):
    print("Calculating hype for %s" % message)


@receiver(twitch_message, sender=TwitchBot)
def unique_users(sender, user, channel, message, **kwargs):
    print("Counting unique users for %s" % channel)


@receiver(twitch_message, sender=TwitchBot)
def sentiment_meter(sender, user, channel, message, **kwargs):
    print("working on sentiment of %s" % message)
