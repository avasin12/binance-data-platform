from datetime import UTC, datetime

import pytest

from acme.utils.time import build_binance_time_window


def test_build_binance_time_window_success():
    data_interval_start = datetime(2026, 7, 30, 0, 0, 0, tzinfo=UTC)
    data_interval_end = datetime(2026, 7, 31, 0, 0, 0, tzinfo=UTC)

    result = build_binance_time_window(data_interval_start, data_interval_end)

    assert result == (1785369600000, 1785455999999)


def test_build_binance_time_window_empty_interval():
    data_interval_start = datetime(2026, 7, 31, 0, 0, 0, tzinfo=UTC)
    data_interval_end = datetime(2026, 7, 31, 0, 0, 0, tzinfo=UTC)

    with pytest.raises(ValueError):
        build_binance_time_window(data_interval_start, data_interval_end)


def test_build_binance_time_window_swapped_interval():
    data_interval_start = datetime(2026, 7, 31, 0, 0, 0, tzinfo=UTC)
    data_interval_end = datetime(2026, 7, 30, 0, 0, 0, tzinfo=UTC)

    with pytest.raises(ValueError):
        build_binance_time_window(data_interval_start, data_interval_end)


@pytest.mark.parametrize(
    "start_tz, end_tz",
    [
        (None, UTC),
        (UTC, None),
        (None, None),
    ],
)
def test_build_binance_time_window_naive_datetimes(start_tz, end_tz):
    data_interval_start = datetime(2026, 7, 30, 0, 0, 0, tzinfo=start_tz)
    data_interval_end = datetime(2026, 7, 31, 0, 0, 0, tzinfo=end_tz)

    with pytest.raises(ValueError):
        build_binance_time_window(data_interval_start, data_interval_end)
