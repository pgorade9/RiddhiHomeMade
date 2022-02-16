from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    password: str
    email: str
    nick_name: Optional[str]
    image_url: Optional[str]


class CurrentUser(BaseModel):
    username: str
    email: Optional[str] = None
    # disabled: Optional[bool] = None
