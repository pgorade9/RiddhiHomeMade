from fastapi import APIRouter
from config import engine
from config import user
from schemas import User
import sqlalchemy


user_routes = APIRouter()


@user_routes.get("/")
def read_root():
    return {"msg": "Hello World"}


@user_routes.get("/user")
def get_user():
    with engine.connect() as connection:
        query = sqlalchemy.select([user])
        results = connection.execute(query).fetchall()
    return results


@user_routes.post("/user")
def add_user(u: User):
    with engine.connect() as connection:
        query = sqlalchemy.insert(user).values((u.user_id, u.user_name, u.email_address, u.nickname))
        connection.execute(query)
        query = sqlalchemy.select([user])
        results = connection.execute(query).fetchall()
    return results[-1]
