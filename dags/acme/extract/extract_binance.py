# /home/avasin/airflow/dags/acme/extract/extract_binance.py

import json
import logging
from pathlib import Path

import requests

from acme.config.settings import settings
from acme.quality.validate_binance import (
    validate_binance_response,
    validate_trades_schema,
)
from acme.storage.paths import build_raw_key
from acme.utils.dag_context import get_dag_context
from acme.utils.time import build_binance_time_window

logger = logging.getLogger(__name__)


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

    request_params = {
        "symbol": symbol,
        "limit": limit,
        "startTime": binance_start_time_ms,
        "endTime": binance_end_time_ms,
    }

    url = settings.binance_api_url

    try:
        response = requests.get(
            url=url,
            params=request_params,
            timeout=30,
        )
        response.raise_for_status()

    except requests.exceptions.Timeout:
        logger.exception("Binance timeout. params=%s", request_params)
        raise

    except requests.exceptions.ConnectionError:
        logger.exception("Binance connection error. params=%s", request_params)
        raise

    except requests.exceptions.HTTPError:
        logger.exception("Binance HTTP error. params=%s", request_params)
        raise

    try:
        response_result = response.json()

    except ValueError:
        logger.exception("Could not decode Binance response as JSON")
        raise

    validate_binance_response(data=response_result, limit=limit)

    validate_trades_schema(data=response_result)

    logger.info("Received %s trades", len(response_result))

    storage_key = build_raw_key(symbol=symbol, data_interval_start=data_interval_start)

    result_path = Path(settings.temp_storage) / storage_key

    result_path.parent.mkdir(parents=True, exist_ok=True)

    with result_path.open("w", encoding="utf-8") as file:
        json.dump(response_result, file, ensure_ascii=False, indent=4)

        logger.info("file seccessfully saved into %s", result_path)

    return {"filepath": str(result_path), "key": storage_key}
