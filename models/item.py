from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from config import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float, index=True)
    stock = Column(Float, index=True)
    image_url = Column(String)
    description = Column(String)
    # owner_id = Column(Integer, ForeignKey("users.id"))
    # owner = relationship("User", backref="items")

    def __repr__(self):
        return f"<Item(name={self.name},description={self.description})>"
