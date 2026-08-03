# /home/avasin/airflow/dags/acme/storage/paths.py


def build_bronze_key(symbol, data_interval_start):

    date_path = data_interval_start.strftime("%Y/%m/%d")

    return f"binance/agg_trades/{symbol}/{date_path}/trades.json"
