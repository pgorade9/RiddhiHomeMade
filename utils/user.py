from fastapi import HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from starlette.datastructures import FormData

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
        return self.get_token(email)

    def get_token(self, email):
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
                              hashed_password=hashing.get_password_hashed(user.password)
                              )
        print("db_user == ",db_user)
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
        print("user = ",user)
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

    def register_user(self, db: Session, form: FormData):
        print(" Registering New User --------------")
        db_user = crud_user.get_user_by_email(db=db, email=form.get('email'))
        if db_user:
            print("User is found and is db_user == ",db_user)
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            print("I am here... as user is None")
            new_user = schemas.UserCreate(id=1,name=form.get('username'), email=form.get('email'), password=form.get('password'))
            current_user = self.create_user(db=db, user=new_user)
            print("i am sending current_user == ", current_user)
            return current_user


crud_user = CRUD()
