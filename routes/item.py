from fastapi import APIRouter
from config import engine
from config import item
from schemas import Item
import sqlalchemy

item_routes = APIRouter()


@item_routes.get("/item")
def get_item():
    with engine.connect() as connection:
        query = sqlalchemy.select([item])
        results = connection.execute(query).fetchall()
    return results


@item_routes.post("/item")
def add_item(i: Item):
    with engine.connect() as connection:
        query = sqlalchemy.insert(item).values((i.id, i.name, i.price, i.stock, i.image_url))
        connection.execute(query)
        query = sqlalchemy.select(item)
        results = connection.execute(query).fetchall()
    return results[-1]


@item_routes.delete("/item/{id}")
def delete_item(id):
    with engine.connect() as connection:
        query = sqlalchemy.delete(item).where(item.c.id == id)
        connection.execute(query)

        query = sqlalchemy.select(item)
        results = connection.execute(query).fetchall()
    return results
