from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

import models
import schemas
from config.db import SessionLocal
from utils import crud_item

item_routes = APIRouter()


# Dependency
def get_db():
    print("SessionLocal : ", SessionLocal)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@item_routes.get("/items")
def get_item(db: Session = Depends(get_db)):
    return crud_item.get_items(db)


@item_routes.post("/item")
def add_item(item: schemas.Item, db: Session = Depends(get_db)):
    return crud_item.create_item(item=item, db=db)


@item_routes.post("/delete/item/{item_id}")
def del_item(item_id: int, db: Session = Depends(get_db)):
    return crud_item.delete_item(item_id=item_id, db=db)


@item_routes.post("/update/item")
def del_item(item: schemas.Item, db: Session = Depends(get_db)):
    return crud_item.update_item(item=item, db=db)
