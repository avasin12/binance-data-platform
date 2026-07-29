#/home/avasin/airflow/dags/acme/storage/paths.py


def build_raw_key(symbol, logical_date, run_id):
    return f"raw/binance/trades/{symbol}/{logical_date.strftime('%Y/%m/%d')}/{run_id}/trades.json"
