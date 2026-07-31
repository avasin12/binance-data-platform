#/home/avasin/airflow/dags/acme/models/binance.py

from pydantic import BaseModel, ConfigDict


class Trade(BaseModel):
    id: int
    price: str
    qty: str
    quoteQty: str
    time: int
    isBuyerMaker: bool
    isBestMatch: bool

    model_config = ConfigDict(extra="forbid")