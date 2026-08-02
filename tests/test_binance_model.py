import pytest
from pydantic import ValidationError

from acme.models.binance import BinanceAggTrade


def test_trade_creation_success():
    trade_data = {
        "a": 6534656718,
        "p": "64762.01",
        "q": "0.00008",
        "f": 27781,
        "l": 27781,
        "T": 1753565088190,
        "m": False,
        "M": True,
    }

    trade = BinanceAggTrade(**trade_data)

    assert trade.aggregate_trade_id == 6534656718
    assert trade.price == "64762.01"
    assert trade.qty == "0.00008"
    assert trade.first_trade_id == 27781
    assert trade.last_trade_id == 27781
    assert trade.time == 1753565088190
    assert trade.is_buyer_maker is False
    assert trade.is_best_match is True


def test_trade_model_invalid_id():
    trade_data = {
        "a": "error",
        "p": "64762.01",
        "q": "0.00008",
        "f": 27781,
        "l": 27781,
        "T": 1753565088190,
        "m": False,
        "M": True,
    }

    with pytest.raises(ValidationError):
        BinanceAggTrade(**trade_data)


def test_trade_model_missing_field():
    trade_data = {
        "a": 1,
        "p": "100",
        "q": "0.5",
        "f": 27781,
        "T": 123456789,
        "m": False,
        "M": True,
    }

    with pytest.raises(ValidationError):
        BinanceAggTrade(**trade_data)


def test_trade_model_extra_field():
    trade_data = {
        "a": 1,
        "p": "100",
        "q": "0.5",
        "f": 27781,
        "l": 27781,
        "T": 123456789,
        "m": False,
        "M": True,
        "unexpected_field": "error",
    }

    with pytest.raises(ValidationError):
        BinanceAggTrade(**trade_data)
