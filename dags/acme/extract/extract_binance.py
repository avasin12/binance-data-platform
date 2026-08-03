# /home/avasin/airflow/dags/acme/extract/extract_binance.py

import json
import logging
from pathlib import Path

from acme.clients.binance_client import fetch_agg_trades_page
from acme.config.settings import settings
from acme.quality.validate_binance import (
    validate_binance_response,
    validate_trades_schema,
)
from acme.storage.paths import build_raw_key
from acme.utils.dag_context import get_dag_context
from acme.utils.time import build_binance_time_window

logger = logging.getLogger(__name__)


def fetch_agg_trades_pagination(url, request_params):

    current_request_params = request_params.copy()

    symbol = request_params["symbol"]
    limit = request_params["limit"]
    start_time_ms = request_params["startTime"]
    end_time_ms = request_params["endTime"]

    current_cursor = None

    all_trades = []

    while True:
        page_response = fetch_agg_trades_page(
            url=url, request_params=current_request_params
        )

        if page_response == []:
            break

        validate_binance_response(data=page_response)
        validate_trades_schema(data=page_response)

        reached_interval_end = False

        for trade in page_response:
            if trade["T"] < start_time_ms:
                continue
            elif trade["T"] > end_time_ms:
                reached_interval_end = True
                break
            else:
                all_trades.append(trade)

        if reached_interval_end:
            break

        last_trade_id = page_response[-1]["a"]

        next_cursor = last_trade_id + 1

        if current_cursor is not None and next_cursor <= current_cursor:
            raise RuntimeError("Pagination cursor did not advance")

        current_cursor = next_cursor

        current_request_params = {
            "symbol": symbol,
            "limit": limit,
            "fromId": current_cursor,
        }

    return all_trades


def extract_market_data():

    dag_context = get_dag_context()

    params = dag_context["params"]

    symbol = params["symbol"]
    limit = params["limit"]
    data_interval_start = dag_context["data_interval_start"]
    data_interval_end = dag_context["data_interval_end"]

    binance_start_time_ms, binance_end_time_ms = build_binance_time_window(
        data_interval_start=data_interval_start, data_interval_end=data_interval_end
    )

    url = settings.binance_api_url

    request_params = {
        "symbol": symbol,
        "limit": limit,
        "startTime": binance_start_time_ms,
        "endTime": binance_end_time_ms,
    }

    response_result = fetch_agg_trades_pagination(
        url=url, request_params=request_params
    )

    logger.info("Received %s trades", len(response_result))

    storage_key = build_raw_key(symbol=symbol, data_interval_start=data_interval_start)

    result_path = Path(settings.temp_storage) / storage_key

    result_path.parent.mkdir(parents=True, exist_ok=True)

    with result_path.open("w", encoding="utf-8") as file:
        json.dump(response_result, file, ensure_ascii=False, indent=4)

        logger.info("file seccessfully saved into %s", result_path)

    return {"filepath": str(result_path), "key": storage_key}
