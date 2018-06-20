from django.dispatch import receiver
from sentimentBot.signals import twitch_message
import logging
logger = logging.getLogger('twitch')


@receiver(twitch_message)
def hype_meter(sender, messages, **kwargs):
    pass


@receiver(twitch_message)
def active_users(sender, messages, **kwargs):
    for message in messages:
        sender.users[message['user']] = sender.users.get(message['user'], 0) + 1


@receiver(twitch_message)
def sentiment_meter(sender, messages, **kwargs):
    pass


@receiver(twitch_message)
def chat_log(sender, messages, **kwargs):
    for line in messages:
        logger.debug("%(channel)s: %(user)s: %(message)s" % line)
