from fastapi import APIRouter, Depends
from config import engine
from config import user
from main import manager
from schemas import User
import sqlalchemy

user_routes = APIRouter()


@user_routes.get("/user")
def get_user():
    with engine.connect() as connection:
        query = sqlalchemy.select(user)
        results = connection.execute(query).fetchall()
    return results


@user_routes.post("/user")
def add_user(u: User):
    with engine.connect() as connection:
        query = sqlalchemy.insert(user).values((u.id, u.name, u.password, u.email, u.nick_name, u.image_url))
        connection.execute(query)
        query = sqlalchemy.select(user)
        results = connection.execute(query).fetchall()
    return results[-1]

@user_routes.delete("/user/{id}")
def delete_user(id, user=Depends(manager)):
    with engine.connect() as connection:
        query = sqlalchemy.delete(user).where(user.c.id == id)
        connection.execute(query)

        query = sqlalchemy.select(user)
        results = connection.execute(query).fetchall()
    return results
