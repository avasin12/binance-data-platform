import pytest
from pydantic import ValidationError

from acme.models.binance import Trade


def test_trade_creation_success():
    trade_data = {
        "id": 6534656718,
        "price": "64762.01",
        "qty": "0.00008",
        "quoteQty": "5.18096080",
        "time": 1753565088190,
        "isBuyerMaker": False,
        "isBestMatch": True,
    }

    trade = Trade(**trade_data)

    assert trade.model_dump() == trade_data


def test_trade_model_invalid_id():
    trade_data = {
        "id": "error",
        "price": "64762.01",
        "qty": "0.00008",
        "quoteQty": "5.18096080",
        "time": 1753565088190,
        "isBuyerMaker": False,
        "isBestMatch": True,
    }

    with pytest.raises(ValidationError):
        Trade(**trade_data)


def test_trade_model_missing_field():
    trade_data = {
        "id": 6534656718,
        "price": "64762.01",
        "qty": "0.00008",
        "quoteQty": "5.18096080",
        "time": 1753565088190,
        "isBuyerMaker": False,
    }

    with pytest.raises(ValidationError):
        Trade(**trade_data)


def test_trade_model_extra_field():
    trade_data = {
        "id": 1,
        "price": "100",
        "qty": "0.5",
        "quoteQty": "5.18096080",
        "time": 123456789,
        "isBuyerMaker": False,
        "isBestMatch": True,
        "unexpected_field": "error"
    }

    with pytest.raises(ValidationError):
        Trade(**trade_data)