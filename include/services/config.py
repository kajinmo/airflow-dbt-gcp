import os
from pathlib import Path
from dotenv import load_dotenv

# For not sensitive info and unlikely to vary between environments

# Load environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    SLACK_TOKEN = os.getenv('SLACK_TOKEN')
    SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', '#alerts')
    DATA_DIR = 'include/data/'
    LOG_FILE = 'logs/engagement_processor.log'

if not Config.SLACK_TOKEN:
    raise ValueError("Missing SLACK_TOKEN in environment variables")