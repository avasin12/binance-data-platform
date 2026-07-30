from pydantic import BaseModel

class Trade(BaseModel):
    id: int
    price: str
    qty: str
    time: int