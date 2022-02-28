from typing import Optional

from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    image_url: Optional[str]
    description:Optional[str]
