from datetime import datetime
from airflow import DAG
from airflow.decorators import dag, task  # IMPORTANTE: adicione essa linha
from airflow.operators.python import PythonOperator
from include.services.config import Config
from include.services.slack_notifier import SlackNotifier

# Argumentos padrão da DAG
@dag(
    start_date=datetime(2025, 1, 1),
    description='Daily engagement report',
    schedule=None,
    catchup=False,
    tags=['engagement']
)
def daily_engagement():
    # Tarefa que envia a mensagem
    def send_slack_message():
        notifier = SlackNotifier()
        success_msg = 'eu sou uma esfirra no airflow'
        notifier.send_message(success_msg)
        return "Mensagem enviada com sucesso!"

    # Operador Python para executar a função
    send_message_task = PythonOperator(
        task_id='send_slack_message',
        python_callable=send_slack_message,
    )

    send_message_task  # Encadeia a tarefa (mesmo que seja só uma)

# Registra a DAG
dag_instance = daily_engagement()