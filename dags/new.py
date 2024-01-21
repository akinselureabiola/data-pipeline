import datetime
import logging

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def hello_world():
    logging.info("Hello World Desmond")

def multiplication():
    print( 5 * 5)

dag = DAG(
    "my_new_dag",
    start_date=datetime.datetime.now() - datetime.timedelta(days=60),
    schedule_interval="@daily"
)

hello_world = PythonOperator(
    task_id="hello_world_task",
    python_callable=hello_world,
    dag=dag
)

multiplication = PythonOperator(
    task_id="multiplication",
    python_callable=multiplication,
    dag=dag
)

hello_world >> multiplication