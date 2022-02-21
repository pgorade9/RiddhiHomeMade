from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from config import Base


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey("users.id"),index=True)
    timestamp = Column(DateTime,nullable=False)
    total = Column(Float,nullable=False)
    status = Column(String,ForeignKey("orders.id"),nullable=False)
