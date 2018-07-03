from django.dispatch import receiver
from sentimentBot.signals import twitch_message
import logging

logger = logging.getLogger('twitch')


@receiver(twitch_message)
def hype_meter(sender, messages, **kwargs):
    sender.update_hype(len(messages))
    print(sender.verbose_hype)


@receiver(twitch_message)
def sentiment_meter(sender, messages, **kwargs):
    for message in messages:
        message.update(sender.polarity_scores(message['message']))
        if message['compound'] != 0:
            sender.update_sentiment(message['compound'])
    print(sender.verbose_sentiment)


@receiver(twitch_message)
def chat_log(sender, messages, **kwargs):
    for line in messages:
        logger.debug("%(channel)s: [%(compound)s] %(user)s: %(message)s" % line)
