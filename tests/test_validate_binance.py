import pytest
from pydantic import ValidationError

from acme.quality.validate_binance import validate_trades_schema


def test_validate_trades_schema_success():
    data = [
        {
            "a": 6534656718,
            "p": "64762.01",
            "q": "0.00008",
            "f": 27781,
            "l": 27781,
            "T": 1753565088190,
            "m": False,
            "M": True,
        }
    ]

    result = validate_trades_schema(data=data)

    assert len(result) == 1
    assert result[0].aggregate_trade_id == 6534656718
    assert result[0].price == "64762.01"


def test_validate_trades_schema_invalid_data():
    data = [
        {
            "a": "error",
            "p": "64762.01",
            "q": "0.00008",
            "f": 27781,
            "l": 27781,
            "T": 1753565088190,
            "m": False,
            "M": True,
        }
    ]

    with pytest.raises(ValidationError):
        validate_trades_schema(data=data)
