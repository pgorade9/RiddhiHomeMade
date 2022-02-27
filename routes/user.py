from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import schemas
from config.db import SessionLocal
from utils.user import crud_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
user_routes = APIRouter()


# Dependency
def get_db():
    print("SessionLocal : ", SessionLocal)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_routes.post('/token')
def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {'access_token': form_data.username + 'token'}


@user_routes.get("/user/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud_user.get_user_by_id(user_id=user_id, db=db)


@user_routes.get("/users")
def get_users(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud_user.get_all_users(db=db)


@user_routes.post("/user")
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)


@user_routes.delete("/delete/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    db_user = crud_user.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User Not Found for the given User Id")
    return crud_user.delete_user(db=db, user_id=user_id)
