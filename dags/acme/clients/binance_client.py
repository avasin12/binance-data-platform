import logging

import requests

logger = logging.getLogger(__name__)


def fetch_agg_trades_page(url, request_params, timeout=30):

    try:
        response = requests.get(
            url=url,
            params=request_params,
            timeout=timeout,
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

    return response_result
