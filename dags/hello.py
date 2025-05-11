from airflow.decorators import dag, task
from datetime import datetime

@dag(
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["example", "hello_world"],
)
def hello_world_dag():
    
    @task
    def say_hello():
        print("Hello, World!")
    
    say_hello()

# Instancia a DAG
hello_world = hello_world_dag()
