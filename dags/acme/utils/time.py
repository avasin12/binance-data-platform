def build_binance_time_window(data_interval_start, data_interval_end):

    if data_interval_start is None or data_interval_end is None:
        raise ValueError("data_interval_start and data_interval_end cannot be None")

    if data_interval_start.utcoffset() is None:
        raise ValueError("data_interval_start must be timezone-aware (provide tzinfo)")
    if data_interval_end.utcoffset() is None:
        raise ValueError("data_interval_end must be timezone-aware (provide tzinfo)")

    if data_interval_start >= data_interval_end:
        raise ValueError("data_interval_start must be less than data_interval_end")

    binance_start_time_ms = int(data_interval_start.timestamp() * 1000)
    binance_end_time_ms = int(data_interval_end.timestamp() * 1000) - 1

    return binance_start_time_ms, binance_end_time_ms
