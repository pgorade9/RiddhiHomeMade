from pydantic import BaseModel


class Item(BaseModel):
    item_id: int
    item_name: str
    item_price: float
    item_stock: int
    item_image_url: str
