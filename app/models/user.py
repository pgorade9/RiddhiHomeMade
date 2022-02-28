from sqlalchemy import Boolean, Column, Integer, String

from app.config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # image_url = Column(String)

    def __repr__(self):
        return f"<User(name={self.id},email={self.email})>"
