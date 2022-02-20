from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from config.db import Base


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False, index=True)
    item_name = Column(String,index=True)
    item_price = Column(Float,index=True)
    quantity = Column(Integer, nullable=False, index=True)
    total = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    status = Column(String, index=True, nullable=False)
    user = relationship("User", backref="orders")
    item = relationship("Item", backref="orders")
