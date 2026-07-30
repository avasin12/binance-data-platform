#/home/avasin/airflow/dags/acme/quality/validate_binance.py

import logging

REQUIRED_FIELDS = {
    "id",
    "price",
    "qty",
    "time"

}

logger = logging.getLogger(__name__)

def validate_binance_response(data, limit):

    if not isinstance(data, list):
        logger.error('Response is not a list')
        raise ValueError('Invalid response format')


    if len(data) == 0:
        logger.warning('Response is empty')
        raise ValueError("Empty Binance response")


    if len(data) != limit:
        logger.warning(f"Recieved {len(data)} trades instead of expected {limit}")


    for trade in data:

        if not isinstance(trade, dict):
            logger.error(
                "Trade is not dict: %s",
                trade
            )
            raise ValueError(
                "Invalid trade format"
            )


        missing_fields = REQUIRED_FIELDS - trade.keys()
    
        if missing_fields:

            logger.error(
                "Trade is missing fields: %s",
                missing_fields
            )
            raise ValueError(
                f"Invalid trade structure. Missing fields: {missing_fields}"
            )

    logger.info("Raw data quality check passed")


