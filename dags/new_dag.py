import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator 

DAG_ID = 'my_mulitiplication'


default_args = {
    'depends_on_past': False,
    'start_date': datetime.datetime(2022, 7, 29),
    'retries': 3,
    'retry_delay': datetime.timedelta(seconds=20)
}

dag = DAG(
    DAG_ID,
    default_args=default_args,
    description='data pipeline for test',
    tags=["testing", "desmond"]
)

def multiplication():
    print(4*4)


def add():
    print(8+67)


multiplication = PythonOperator(
dag=dag,
task_id='multiplication',
python_callable=multiplication
)

add = PythonOperator(
dag=dag,
task_id='add',
python_callable=add
)

multiplication >> add