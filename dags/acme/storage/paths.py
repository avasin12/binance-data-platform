#/home/avasin/airflow/dags/acme/storage/paths.py


def build_raw_key(symbol, logical_date, run_id):

    date_path = logical_date.strftime('%Y/%m/%d')

    return f"raw/binance/trades/{symbol}/{date_path}/{run_id}/trades.json"
