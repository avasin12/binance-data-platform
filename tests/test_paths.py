from datetime import datetime

from acme.storage.paths import build_raw_key


def test_build_raw_key_creates_expected_path():
    logical_date = datetime(2026, 7, 30)

    result = build_raw_key(
        symbol="BTCUSDT",
        logical_date=logical_date,
    )

    assert result == (
        "raw/binance/trades/"
        "BTCUSDT/"
        "2026/07/30/"
        "trades.json"
    )