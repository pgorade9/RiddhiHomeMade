from typing import Optional

from pydantic import BaseModel


# Note the implementation of SOLID principles (Interface seggregation)
class UserBase(BaseModel):
    id: int
    name: str
    email: str
    image_url: Optional[str]


class UserCreate(UserBase):
    password: str


class User(UserBase):
    class Config:
        orm_mode = True
