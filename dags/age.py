import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator 
import awswrangler

DAG_ID = 'age_check'


default_args = {
    'depends_on_past': False,
    'start_date': datetime.datetime(2022, 7, 29),
    'retries': 3,
    'retry_delay': datetime.timedelta(seconds=10)
}

dag = DAG(
    DAG_ID,
    default_args=default_args,
    description='subscription attributes data to the lake',
    tags=["age_calculator", "desmond"]
)

def multiplication():
    print( 5 * 5)

def add():
    print(2 + 2)

def minus():
    print(5-2)

def age_check(**context):
    birth_year = int(Variable.get('birth_year'))
    current_year = 2022
    age = current_year - birth_year
    task_instance = context['ti']
    task_instance.xcom_push(key='our_key', value=age)

def total_sale(**context):
    task_instance = context['ti']
    old_ages = task_instance.xcom_pull(key='our_key', task_ids='age_check')
    new_ages = old_ages + 50
    task_instance = context['ti']
    task_instance.xcom_push(key='our_key', value=new_ages)
    

def age_division(**context):
    task_instance = context['ti']
    age_divisible = task_instance.xcom_pull(key='our_key', task_ids='total_sale')
    age_diff = age_divisible / 7
    return age_diff


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

minus = PythonOperator(
    dag=dag,
    task_id='minus',
    python_callable=minus
)

age_check = PythonOperator(
    dag=dag,
    task_id='age_check',
    python_callable=age_check
)


total_sale = PythonOperator(
    dag=dag,
    task_id='total_sale',
    python_callable=total_sale
)

age_division = PythonOperator(
    dag=dag,
    task_id='age_division',
    python_callable=age_division 
)



multiplication >> add >> minus >> age_check >> total_sale >> age_division
 