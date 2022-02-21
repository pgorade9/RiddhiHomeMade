from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from sqlalchemy.orm import relationship

from config import Base


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey("users.id"),index=True)
    timestamp = Column(DateTime,nullable=False)
    total = Column(Float,nullable=False)
    payment_status = Column(String,nullable=False)

    def __repr__(self):
        return f"<Invoice(id={self.id},user_id={self.user_id},total={self.total},payment_status={self.payment_status})>"

