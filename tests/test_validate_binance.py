import pytest

from acme.quality.validate_binance import validate_binance_response


def test_validate_binance_response_success():
    data = [
        {
            "id": 1,
            "price": "100",
            "qty": "0.5",
            "time": 123456789
        }
    ]
    validate_binance_response(data=data, limit=1)


def test_validate_binance_response_missing_required_field():
    data = [
        {
            "id": 1,
            "price": "100",
            "qty": "0.5",
        }
    ]
    with pytest.raises(ValueError):
        validate_binance_response(data=data, limit=1)