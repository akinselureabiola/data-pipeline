import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator 

DAG_ID = 'addition'


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

def addition():
    print(4+5)


addition = PythonOperator(
dag=dag,
task_id='addition',
python_callable=addition
)

addition