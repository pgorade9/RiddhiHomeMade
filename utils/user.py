from fastapi import HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

import models
import schemas
from config import settings
from utils import hashing


class CRUD:

    def authenticate_user(self, db: Session, email: str, password: str):
        db_user = db.query(models.User).filter(models.User.email == email).first()
        if not db_user:
            return {"User not recognized. Please register"}
        elif not hashing.verify_password(password, db_user.hashed_password):
            return {"Invalid Username or Password"}
        return jwt.encode({"sub": email}, settings.SECRET_KEY, settings.ALGORITHM)

    def get_current_user(self, token: str, db: Session):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        print("i am at get_current_user")
        try:
            token = token.split(None, 1)[1]
            data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
            email = data.get("sub")
        except JWTError:
            raise credentials_exception
        print("decoded email = ", email)
        user = db.query(models.User).filter(models.User.email == email).first()
        if user is None:
            raise credentials_exception
        return schemas.User(id=user.id, email=user.email, name=user.name)

    def create_user(self, db: Session, user: schemas.UserCreate) -> models.User:
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


crud_user = CRUD()
