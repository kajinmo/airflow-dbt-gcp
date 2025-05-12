from datetime import datetime
import logging
import pandas as pd
import os

from include.services.config import Config
from include.services.slack_notifier import SlackNotifier
from include.utils.file_handlers import get_most_recent_filepath, read_data_file
from include.validator.validator import EngagementValidator

from airflow.decorators import dag, task
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator


# Logging config
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# DAG config
@dag(
    start_date=datetime(2025, 1, 1),
    description='Daily engagement report',
    schedule=None,
    catchup=False,
    tags=['engagement']
)
def engagement_validation_dag():
    @task()
    def get_latest_filepath() -> str:
        logger.info("Fetching the latest file")
        filepath = get_most_recent_filepath(
            directory_path=Config.DATA_DIR,
            file_type='csv'
        )
        logger.info(f"File found: {filepath}")
        return filepath

    @task()
    def read_file(filepath: str) -> pd.DataFrame:
        logger.info("Reading file")
        df = read_data_file(
            file_path=filepath,
            file_type='csv',
            sep=','
        )
        logger.info(f"{len(df)} loaded records")
        return df

    @task()
    def validate(df: pd.DataFrame) -> dict:
        logger.info("Validando os dados")
        validator = EngagementValidator(df)
        validator.validate()
        valid_data = validator.valid_data

        logger.info(f"{len(valid_data)} registros válidos")
        return {
            "valid_count": len(valid_data),
            "error_count": len(validator.errors),
            "errors": validator.errors,
            "valid_data": valid_data
        }


    @task()
    def slack_msg_validation_raw(validation_results: dict):
        notifier = SlackNotifier()
        success_msg = (
            f"Validation completed\n"
            f"• Valid records: {validation_results['valid_count']}\n"
            f"• Errors found: {validation_results['error_count']}"
        )
        notifier.send_message(success_msg)
        if validation_results['errors']:
            notifier.send_error_report(validation_results['errors'])
        logger.info("Notificação enviada com sucesso")

    @task()
    def save_temp_validated_csv(df_dict: dict) -> str:
        df = pd.DataFrame(df_dict["valid_data"])
        os.makedirs("/tmp/data", exist_ok=True)
        filename = f"validated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join("/tmp/data", filename)
        df.to_csv(filepath, index=False, encoding='utf-8')
        logger.info(f"File temporarily saved in: {filepath}")
        return filepath
    
    # Chaining tasks
    filepath = get_latest_filepath()
    df = read_file(filepath)
    results = validate(df)
    slack_msg_validation_raw(results)
    csv_path = save_temp_validated_csv(results)

    upload_csv_to_gcs = LocalFilesystemToGCSOperator(
        task_id='upload_validated_csv_to_gcs',
        src=csv_path,
        dst='raw/engagement.csv',
        bucket=Config.GCP_BUCKET_NAME,
        gcp_conn_id='gcp',
        mime_type='text/csv',
    )

    # Conectando o operador ao DAG
    csv_path >> upload_csv_to_gcs


# Instância da DAG
dag_instance = engagement_validation_dag()