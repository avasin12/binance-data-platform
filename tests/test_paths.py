from datetime import datetime

from acme.storage.paths import build_bronze_key


def test_build_bronze_key_creates_expected_path():
    data_interval_start = datetime(2026, 7, 30)

    result = build_bronze_key(
        symbol="BTCUSDT",
        data_interval_start=data_interval_start,
    )

    assert result == ("binance/agg_trades/BTCUSDT/2026/07/30/trades.json")
