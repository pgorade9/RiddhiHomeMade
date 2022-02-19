from pydantic import BaseModel


class Order(BaseModel):
    name: str
    user: str
    quantity: int
    price: float
    total: float
    invoice_id = int
