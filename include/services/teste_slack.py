from config import Config
from slack_notifier import SlackNotifier
notifier = SlackNotifier()
success_msg = ('eu sou uma esfirraaaa')
notifier.send_message(success_msg)