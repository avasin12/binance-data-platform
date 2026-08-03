from unittest.mock import Mock, patch

from acme.clients.binance_client import fetch_agg_trades_page


def test_fetch_agg_trades_page_success():
    expected_data = [
        {
            "a": 4027420997,
            "p": "62887.88000000",
            "q": "0.00007000",
            "f": 6550162200,
            "l": 6550162200,
            "T": 1785445999999,
            "m": False,
            "M": True,
        }
    ]

    fake_response = Mock()
    fake_url = "https://example.test/api/v3/aggTrades"

    fake_response.json.return_value = expected_data
    test_params = {
        "symbol": "BTCUSDT",
        "limit": 1000,
        "startTime": 1785369600000,
        "endTime": 1785455999999,
    }

    with patch("acme.clients.binance_client.requests.get") as mock_get:
        mock_get.return_value = fake_response

        result = fetch_agg_trades_page(
            url=fake_url,
            request_params=test_params,
        )

        assert result == expected_data

        mock_get.assert_called_once_with(url=fake_url, params=test_params, timeout=30)

        fake_response.raise_for_status.assert_called_once_with()
        fake_response.json.assert_called_once_with()
