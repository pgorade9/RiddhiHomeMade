import datetime

from pydantic.main import BaseModel


class Invoice(BaseModel):
    id: int
    user_id: int
    timestamp: datetime.datetime
    total: float
    payment_status: str