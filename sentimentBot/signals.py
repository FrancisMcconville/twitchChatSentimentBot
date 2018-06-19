from django.dispatch import Signal

twitch_message = Signal(providing_args=["user", "channel", "message"])
