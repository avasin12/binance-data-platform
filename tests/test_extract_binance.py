from unittest.mock import call, patch

from acme.extract.extract_binance import fetch_agg_trades_pagination


def test_fetch_agg_trades_pagination_stops_at_interval_end():
    fake_url = "https://example.test/api/v3/aggTrades"
    initial_params = {
        "symbol": "BTCUSDT",
        "limit": 2,
        "startTime": 1000,
        "endTime": 1999,
    }

    page_1 = [
        {
            "a": 100,
            "p": "100.00",
            "q": "0.01",
            "f": 100,
            "l": 100,
            "T": 1100,
            "m": False,
            "M": True,
        },
        {
            "a": 101,
            "p": "100.00",
            "q": "0.01",
            "f": 101,
            "l": 101,
            "T": 1200,
            "m": False,
            "M": True,
        },
    ]

    page_2 = [
        {
            "a": 102,
            "p": "100.00",
            "q": "0.01",
            "f": 102,
            "l": 102,
            "T": 1300,
            "m": False,
            "M": True,
        },
        {
            "a": 103,
            "p": "100.00",
            "q": "0.01",
            "f": 103,
            "l": 103,
            "T": 2000,
            "m": False,
            "M": True,
        },
    ]

    expected_result = [
        page_1[0],
        page_1[1],
        page_2[0],
    ]

    with patch("acme.extract.extract_binance.fetch_agg_trades_page") as mock_fetch:
        mock_fetch.side_effect = [page_1, page_2]

        result = fetch_agg_trades_pagination(
            url=fake_url,
            request_params=initial_params,
        )

    assert result == expected_result
    assert mock_fetch.call_count == 2
    assert mock_fetch.call_args_list == [
        call(
            url=fake_url,
            request_params=initial_params,
        ),
        call(
            url=fake_url,
            request_params={
                "symbol": "BTCUSDT",
                "limit": 2,
                "fromId": 102,
            },
        ),
    ]


def test_fetch_agg_trades_pagination_continues_after_short_page_and_stops_on_empty():
    fake_url = "https://example.test/api/v3/aggTrades"
    initial_params = {
        "symbol": "BTCUSDT",
        "limit": 3,
        "startTime": 1000,
        "endTime": 1999,
    }

    page_1 = [
        {
            "a": 100,
            "p": "100.00",
            "q": "0.01",
            "f": 100,
            "l": 100,
            "T": 1100,
            "m": False,
            "M": True,
        },
        {
            "a": 101,
            "p": "100.00",
            "q": "0.01",
            "f": 101,
            "l": 101,
            "T": 1200,
            "m": False,
            "M": True,
        },
        {
            "a": 102,
            "p": "100.00",
            "q": "0.01",
            "f": 102,
            "l": 102,
            "T": 1300,
            "m": False,
            "M": True,
        },
    ]

    page_2 = [
        {
            "a": 103,
            "p": "100.00",
            "q": "0.01",
            "f": 103,
            "l": 103,
            "T": 1400,
            "m": False,
            "M": True,
        }
    ]

    page_3 = []

    expected_result = [
        page_1[0],
        page_1[1],
        page_1[2],
        page_2[0],
    ]

    with patch("acme.extract.extract_binance.fetch_agg_trades_page") as mock_fetch:
        mock_fetch.side_effect = [page_1, page_2, page_3]

        result = fetch_agg_trades_pagination(
            url=fake_url,
            request_params=initial_params,
        )

    assert result == expected_result
    assert mock_fetch.call_count == 3
    assert mock_fetch.call_args_list == [
        call(
            url=fake_url,
            request_params=initial_params,
        ),
        call(
            url=fake_url,
            request_params={
                "symbol": "BTCUSDT",
                "limit": 3,
                "fromId": 103,
            },
        ),
        call(
            url=fake_url,
            request_params={
                "symbol": "BTCUSDT",
                "limit": 3,
                "fromId": 104,
            },
        ),
    ]
