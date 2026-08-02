# /home/avasin/airflow/dags/dag_extract_binance.py

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from acme.clients.minio_client import upload_to_minio
from acme.extract.extract_binance import extract_market_data
from acme.storage.files import delete_local_files
from acme.utils.dag_params import DEFAULT_BINANCE_PARAMS
from acme.utils.notification import notify_on_failed

default_args = {
    "owner": "avasin",
    "retries": 0,
    "retry_delay": timedelta(minutes=2),
    "on_failure_callback": notify_on_failed,
}

tags = ["critical", "etl"]

FILE_INFO_TEMPLATE = (
    "{{ ti.xcom_pull(task_ids='extract_binance_trades', key='return_value') }}"
)

with DAG(
    dag_id="dag_extract_binance",
    description="Extract Binance trades information and save raw data to MinIO",
    schedule="@daily",
    start_date=datetime(2026, 7, 1),
    catchup=False,
    tags=tags,
    max_active_runs=1,
    default_args=default_args,
    dagrun_timeout=timedelta(hours=2),
    params=DEFAULT_BINANCE_PARAMS,
    render_template_as_native_obj=True,
) as dag:
    extract_binance_trades_task = PythonOperator(
        task_id="extract_binance_trades",
        python_callable=extract_market_data,
    )

    upload_to_minio_task = PythonOperator(
        task_id="upload_to_minio",
        python_callable=upload_to_minio,
        op_kwargs={"file_info": FILE_INFO_TEMPLATE},
    )

    delete_local_file_task = PythonOperator(
        task_id="delete_local_files",
        python_callable=delete_local_files,
        op_kwargs={"file_info": FILE_INFO_TEMPLATE},
    )
    extract_binance_trades_task >> upload_to_minio_task >> delete_local_file_task
