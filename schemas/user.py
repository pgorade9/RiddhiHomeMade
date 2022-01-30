from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    password: str
    email: str
    nick_name: Optional[str]
    image_url: Optional[str]
