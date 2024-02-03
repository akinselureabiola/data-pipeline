import requests
import json
import pandas as pd
from boto3.s3.transfer import S3Transfer
import boto3
import datetime
from sqlalchemy import Table
from sqlalchemy.engine.base import Engine as sql_engine
import awswrangler as wr
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator 
from boto3.session import Session
from sqlalchemy import create_engine

DAG_ID = 'api_file-extract-and-upload'


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
    tags=["extract_file", "upload_file"]
)

def extract_file():
    url = "http://universities.hipolabs.com/search?country=United+States"
    response = requests.get(url)
    data = response.text

    # converting string to JSON
    parsed = json.loads(data)
    json_data = print(json.dumps(parsed))
    df = pd.DataFrame({'col':parsed})

    # Convert DataFrame to Csv file format
    df_csv = df.to_csv('./logs/uni.csv', index=False)

    #Convert CSV file to Paquet file format
    df_paquet = df.to_parquet('./logs/uni.parquet', index=False)


def upload_file_to_s3():
    
    client = boto3.client('s3')
    transfer = S3Transfer(client)

    s3_client = boto3.client('s3', aws_access_key_id=Variable.get('ACCESS_KEY'), aws_secret_access_key=Variable.get('SECRET_KEY'))
    transfer = S3Transfer(s3_client)
    transfer.upload_file('./logs/uni.parquet', 'staging-olist', 'uni.parquet', extra_args={'ServerSideEncryption': "AES256"})


def transfer_file():
    session = boto3.session.Session(aws_access_key_id=Variable.get('ACCESS_KEY'), 
                      aws_secret_access_key=Variable.get('SECRET_KEY')
                     )
    # read file using awswrangler
    df = wr.s3.read_parquet(path='s3://staging-olist/uni.parquet', boto3_session=session)
    
    # transfer file from s3 to postgres rds db
    conn = create_engine("postgresql+psycopg2://staging_db:DnrbWdUcaZxyIc7v@postgres.cnelwn14hnqh.eu-central-1.rds.amazonaws.com:5432/main")
    new_df = df.to_sql("old-uni-file", con=conn, schema="olist")
    return new_df
    

extract_file = PythonOperator(
    dag=dag,
    task_id='extract_file',
    python_callable=extract_file
)

upload_file_to_s3 = PythonOperator(
    dag=dag,
    task_id='upload_file_to_s3',
    python_callable=upload_file_to_s3
)

transfer_file = PythonOperator(
    dag=dag,
    task_id='transfer_file',
    python_callable=transfer_file
)


extract_file >> upload_file_to_s3 >> transfer_file