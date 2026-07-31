import pytest
from pydantic import ValidationError

from acme.quality.validate_binance import validate_trades_schema


def test_validate_trades_schema_success():
    data = [
        {
            "id": 6534656718,
            "price": "64762.01",
            "qty": "0.00008",
            "quoteQty": "5.18096080",
            "time": 1753565088190,
            "isBuyerMaker": False,
            "isBestMatch": True,
        }
    ]

    result = validate_trades_schema(data=data)

    assert len(result) == 1
    assert result[0].id == 6534656718
    assert result[0].price == "64762.01"


def test_validate_trades_schema_invalid_data():
    data = [
        {
            "id": "error",
            "price": "64762.01",
            "qty": "0.00008",
            "quoteQty": "5.18096080",
            "time": 1753565088190,
            "isBuyerMaker": False,
            "isBestMatch": True,
        }
    ]

    with pytest.raises(ValidationError):
        validate_trades_schema(data=data)