import boto3
import awswrangler as wr


def read_s3_file():
    session = boto3.session.Session(aws_access_key_id="AKIASVY4A2TKSPFHTZWM", 
                                    aws_secret_access_key="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")
    df = wr.s3.read_csv(path='s3://staging-olist/olist_customers_dataset.csv', boto3_session=session)
    return df.shape
