# /home/avasin/airflow/dags/acme/utils/dag_context.py
from airflow.sdk import get_current_context


def get_dag_context():
    context = get_current_context()

    result = {
        "params": context["params"],
        "logical_date": context["logical_date"],
        "run_id": context["run_id"],
        "task_instance": context["ti"],
        "data_interval_start": context["data_interval_start"],
        "data_interval_end": context["data_interval_end"],
    }

    return result
