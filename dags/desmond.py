import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator 
import boto3
from boto3.session import Session


DAG_ID = 'read_s3_file'


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
    tags=["read_s3", "read_file"]
)

def generic_s3_client(aws_access_key_id, aws_secret_access_key):
    client = boto3.client(
    's3',
    aws_access_key_id=Variable.get('ACCESS_KEY'),
    aws_secret_access_key=Variable.get('SECRET_KEY'))
    
    return client
        

def list_s3_object(bucket_name, bucket_prefix, aws_access_key_id, aws_secret_access_key):
    instantiate = generic_s3_client(aws_access_key_id, aws_secret_access_key)
    s3_objects = instantiate.list_objects(Bucket = bucket_name, Prefix = bucket_prefix)
    
    return s3_objects



list_s3_object = PythonOperator(
    dag=dag,
    task_id='list_s3_object',
    python_callable=list_s3_object
)


generic_s3_client >> list_s3_object