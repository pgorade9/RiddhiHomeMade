from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    user_name: str
    email_address: str
    nickname: str
