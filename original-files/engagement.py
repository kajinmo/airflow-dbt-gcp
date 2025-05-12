import logging
from include.services.config import Config
from utils.file_handlers import get_most_recent_filepath, read_data_file
from validator.validator import EngagementValidator
from services.slack_notifier import SlackNotifier

data_directory = Config.DATA_DIR
file_extension = 'csv'
sep=','

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


notifier = SlackNotifier()

try:
    logger.info("Starting engagement data processing")

    # 1. Get the data filepath
    latest_filepath = get_most_recent_filepath(
        directory_path=data_directory,
        file_type=file_extension
    )
    print(f"Processing: {latest_filepath}")
    

    # 2. Read the file to DataFrame
    df = read_data_file(
        file_path=latest_filepath,
        file_type=file_extension,
        sep=sep
    )
    logger.info(f"Loaded {len(df)} records")


    # 3. Validate
    validator = EngagementValidator(df)
    valid_data = validator.validate()


    # 4. Report results - raw
    success_msg = (
            f"Validation completed\n"
            f"• Valid records: {len(valid_data)}\n"
            #f"• Errors found: {len(validator.errors)}"
        )
    notifier.send_message(success_msg)
    if validator.errors:
        notifier.send_error_report(validator.errors)
    logger.info("Processing completed successfully")

    


except Exception as e:
    error_msg = f"Processing failed: {str(e)}"
    logger.error(error_msg)
    notifier.send_message(error_msg)