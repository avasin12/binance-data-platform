#/home/avasin/airflow/dags/acme/quality/validate_binance.py

import logging

from acme.models.binance import BinanceAggTrade

logger = logging.getLogger(__name__)

def validate_trades_schema(data):
    result = []

    for trade in data:
        result.append(BinanceAggTrade(**trade))

    return result




def validate_binance_response(data, limit):

    if not isinstance(data, list):
        logger.error("Response is not a list")
        raise ValueError("Invalid response format")


    if len(data) == 0:
        logger.warning("Response is empty")
        raise ValueError("Empty Binance response")


    if len(data) != limit:
        logger.warning(
            "Received %s trades instead of expected %s",
            len(data),
            limit,
        )


    logger.info(
        "Raw data quality check passed. Trades count: %s",
        len(data),
    )