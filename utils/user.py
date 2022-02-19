from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
import schemas
from schemas import UserCreate
from utils import hashing


class CRUD:

    def create_user(self, db: Session, user: UserCreate) -> models.User:
        db_user = models.User(name=user.name, email=user.email,
                              hashed_password=hashing.get_password_hashed(user.password),
                              image_url=user.image_url)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        u = db.query(models.User).filter(models.User.email == user.email).first()
        current_user = schemas.User(id=u.id, email=u.email, name=u.name)
        return current_user

    def get_user_by_id(self, db: Session, user_id: int):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        print("user = ", user)
        return schemas.User(id=user.id, email=user.email, name=user.name)

    def get_user_by_email(self, db: Session, email: str):
        user = db.query(models.User).filter(models.User.email == email).first()
        if user:
            return schemas.User(id=user.id, email=user.email, name=user.name)

    def get_all_users(self, db: Session):
        users = db.query(models.User).all()
        return users

    def delete_user(self, db: Session, user_id: int):
        result = db.query(models.User).filter(models.User.id == user_id).first()
        db.delete(result)
        db.commit()
        return result


crud = CRUD()
