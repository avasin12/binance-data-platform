#/home/avasin/airflow/dags/acme/utils/notification.py
#TODO


import logging
logger = logging.getLogger(__name__)


def notify_on_failed(context):

    dag_id = context["dag"].dag_id
    task_id = context["task_instance"].task_id

    logger.error(
        "DAG %s failed on task %s",
        dag_id,
        task_id
    )