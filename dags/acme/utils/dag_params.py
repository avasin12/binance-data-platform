# /home/avasin/airflow/dags/acme/utils/dag_params.py


from airflow.sdk import Param

DEFAULT_BINANCE_PARAMS = {
    "symbol": Param(
        title="Symbol",
        default="BTCUSDT",
        type="string",
        minLength=3,
        maxLength=30,
        pattern="^[A-Z0-9]+$",
    ),
    "limit": Param(
        title="Maximum trades per API page",
        default=1000,
        type="integer",
        minimum=1,
        maximum=1000,
    ),
}
