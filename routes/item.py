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
        query = sqlalchemy.insert(item).values((i.item_id, i.item_name, i.item_price, i.item_stock,i.item_image_url))
        connection.execute(query)
        query = sqlalchemy.select([item])
        results = connection.execute(query).fetchall()
    return results[-1]