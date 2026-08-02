# /home/avasin/airflow/dags/acme/models/binance.py

from pydantic import BaseModel, ConfigDict, Field


class BinanceAggTrade(BaseModel):
    aggregate_trade_id: int = Field(alias="a")
    price: str = Field(alias="p")
    qty: str = Field(alias="q")
    first_trade_id: int = Field(alias="f")
    last_trade_id: int = Field(alias="l")
    time: int = Field(alias="T")
    is_buyer_maker: bool = Field(alias="m")
    is_best_match: bool = Field(alias="M")

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
    )
