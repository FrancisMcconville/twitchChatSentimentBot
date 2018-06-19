from django.dispatch import receiver
from sentimentBot.signals import twitch_message
from sentimentBot.bot import TwitchBot


@receiver(twitch_message, sender=TwitchBot)
def hype_meter(sender, messages, **kwargs):
    pass


@receiver(twitch_message, sender=TwitchBot)
def unique_users(sender, messages, **kwargs):
    pass


@receiver(twitch_message, sender=TwitchBot)
def sentiment_meter(sender, messages, **kwargs):
    for line in messages:
        print("%(user)s: %(message)s" % line)
