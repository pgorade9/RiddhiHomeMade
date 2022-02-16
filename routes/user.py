from fastapi import APIRouter, Depends
from passlib.context import CryptContext

from config import engine, user
from main import manager
from schemas import User
import sqlalchemy

user_routes = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@user_routes.get("/user")
def get_user():
    with engine.connect() as connection:
        query = sqlalchemy.select(user)
        results = connection.execute(query).fetchall()
    return results


def get_password_hashed(password):
    return pwd_context.hash(password)


@user_routes.post("/user")
def add_user(u: User):
    with engine.connect() as connection:
        query = sqlalchemy.insert(user).values(
            (u.id, u.name, get_password_hashed(u.password), u.email, u.nick_name, u.image_url))
        connection.execute(query)
        query = sqlalchemy.select(user)
        results = connection.execute(query).fetchall()
    return results[-1]


@user_routes.delete("/user/{id}")
def delete_user(id, current_user=Depends(manager)):
    print("current User = ", current_user)
    with engine.connect() as connection:
        query = sqlalchemy.delete(user).where(user.c.id == id)
        connection.execute(query)

        query = sqlalchemy.select(user)
        results = connection.execute(query).fetchall()
    return results
