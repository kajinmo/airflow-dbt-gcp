import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from include.services.config import Config

class SlackNotifier:
    def __init__(self):
        self.client = WebClient(token=Config.SLACK_TOKEN)
        self.channel = Config.SLACK_CHANNEL
        self.logger = logging.getLogger(__name__)

    def send_message(self, text: str) -> bool:
        try:
            response = self.client.chat_postMessage(
                channel=self.channel,
                text=text
            )
            self.logger.info(f"Slack message sent: {text}")
            return True
        except SlackApiError as e:
            self.logger.error(f"Slack API error: {e.response['error']}")
            return False

    def send_error_report(self, errors: list) -> bool:
        if not errors:
            return False
            
        error_text = "*Data Validation Errors Report*\n"
        error_text += f"• Total errors: {len(errors)}\n"
        error_text += "• Sample errors:\n"
        
        for error in errors[:5]:  # Send first 5 errors as sample
            error_text += f"  - Row {error['row']}: {error['error']}\n"
        
        return self.send_message(error_text)