#/home/avasin/airflow/dags/acme/clients/minio_client.py

from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.sdk import Variable
from botocore.exceptions import ClientError
from pathlib import Path


import logging

logger = logging.getLogger(__name__)

def get_minio_client():
    hook = S3Hook(aws_conn_id="minio_client")
    minio_client = hook.get_conn()

    return minio_client



def upload_to_minio(file_info):

    minio_client = get_minio_client()

    filepath = file_info["filepath"]
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(
            f"File does not exist: {filepath}"
        )

    if path.stat().st_size == 0:
        raise ValueError(
            f"File is empty: {filepath}"
        )


    key = file_info["key"]

    bucket = Variable.get("minio_raw_bucket")
    try:

        minio_client.upload_file(filepath, bucket, key)
        logger.info(f'Uploaded {file_info} to {key}')

        minio_client.head_object(
            Bucket=bucket,
            Key=key
        )
        logger.info("File exists in MinIO")

    
    except ClientError:
        logger.exception("Could not upload file to MinIO")
        raise