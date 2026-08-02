# /home/avasin/airflow/dags/acme/storage/paths.py


def build_raw_key(symbol, data_interval_start):

    date_path = data_interval_start.strftime("%Y/%m/%d")

    return f"raw/binance/trades/{symbol}/{date_path}/trades.json"
