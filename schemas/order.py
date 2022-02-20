from pydantic import BaseModel


class Order(BaseModel):
    id: int
    item_id: int
    item_name: str
    quantity: int
    item_price: float
    total: float
    user_id = int
