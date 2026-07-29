#/home/avasin/airflow/dags/acme/extract/extract_binance.py

import requests
import logging
import json
from pathlib import Path
from acme.utils.dag_context import get_dag_context
from airflow.sdk import Variable
from acme.quality.validate_binance import validate_binance_response
from acme.storage.paths import build_raw_key
logger = logging.getLogger(__name__)



def extract_market_data():

    dag_context = get_dag_context()

    params = dag_context["params"]

    symbol = params["symbol"]
    limit = params["limit"]

    logical_date = dag_context["logical_date"]
    run_id = dag_context["run_id"]


    request_params = {
        "symbol": symbol,
        "limit": limit
    }
    url = Variable.get("binance_api_url")

    try:
        response = requests.get(
            url=url,
            params=request_params,
            timeout=30,
        )
        response.raise_for_status()



    except requests.exceptions.Timeout:
        logger.exception(
            "Binance timeout. params=%s",
            request_params
        )
        raise


    except requests.exceptions.ConnectionError:
        logger.exception(
            "Binance connection error. params=%s",
            request_params
        )
        raise


    except requests.exceptions.HTTPError:
        logger.exception(
            "Binance HTTP error. params=%s",
            request_params
        )
        raise

    try:
        response_result = response.json()

    except ValueError:
        logger.exception(
            "Could not decode Binance response as JSON"
        )
        raise

    validate_binance_response(data=response_result, limit=limit)

    logger.info("Received %s trades", len(response_result))


    storage_key = build_raw_key(symbol=symbol, logical_date=logical_date, run_id=run_id)

    result_path = Path("/mnt/ceph/temp_jsons") / storage_key

    result_path.parent.mkdir(parents=True, exist_ok=True)

    with result_path.open('w', encoding='utf-8') as file:
        json.dump(response_result, file, ensure_ascii=False, indent=4)

        logger.info('file seccessfully saved into %s', result_path)

    return {
        "filepath": str(result_path),
        "key": storage_key
    }

