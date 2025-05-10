import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('SLACK_TOKEN')
if not token:
    raise ValueError("SLACK_TOKEN não encontrado")

client = WebClient(token=token)

try:
    response = client.chat_postMessage(channel='#alerts', text="Hello World!")
except SlackApiError as e:
    print(f"Erro ao enviar mensagem: {e.response['error']}")