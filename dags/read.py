import datetime
import pandas as pd
from sqlalchemy import Table
from sqlalchemy.engine.base import Engine as sql_engine
import awswrangler as wr
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator 
import boto3
from boto3.session import Session
from sqlalchemy import create_engine



DAG_ID = 'read_s3_data'


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
    tags=["read_s3_datas", "read_file2"]
)

def read_s3_file():
    session = boto3.session.Session(aws_access_key_id=Variable.get('ACCESS_KEY'), 
                      aws_secret_access_key=Variable.get('SECRET_KEY')
                     )
    df = wr.s3.read_csv(path='s3://staging-olist/customer/olist_customers_dataset.csv', boto3_session=session)
    
    # create a connection from postgres URI
    conn = create_engine("postgresql+psycopg2://staging_db:DnrbWdUcaZxyIc7v@postgres.cnelwn14hnqh.eu-central-1.rds.amazonaws.com:5432/main")
    new_df = df.to_sql("old_customer", con=conn, schema="olist")
    return new_df




read_s3_file = PythonOperator(
    dag=dag,
    task_id='read_s3_data',
    python_callable=read_s3_file
)


read_s3_file