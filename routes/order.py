from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from config.db import SessionLocal
from models import Message
from routes.home import templates
from utils import crud_user, crud_item, crud_order

order_routes = APIRouter()


# Dependency
def get_db():
    print("SessionLocal : ", SessionLocal)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@order_routes.post("/orders/{item_id}")
async def add_order(request: Request, item_id: int, db: Session = Depends(get_db)):
    print("Hey I am listening --- ")
    item = crud_item.get_item_by_id(item_id=item_id, db=db)
    form = await request.form()
    quantity = float(form.get("quantity"))
    print("quantity = ", quantity)
    products = crud_item.get_items(db)
    token = request.cookies.get("access_token")
    current_user = crud_user.get_current_user(token=token, db=db)
    new_order = crud_order.create_order(db=db, item_id=item_id, quantity=quantity, user=current_user)
    print("I passed create order step")
    orders = crud_order.get_orders(db, current_user)
    if new_order:
        print("I should not be seen")
        crud_item.update_stock(order_id=new_order.id, quantity=quantity, db=db)
        messages = [Message(message=f"You Added Product to Cart for \"{new_order.item_name}\" ", flag="success")]
        return templates.TemplateResponse("index.html",
                                          {"request": request, "products": products, "orders": orders,
                                           "current_user": current_user, "messages": messages})
    messages = [Message(message=f"Item Out of Stock for \"{item.name}\" ", flag="danger")]
    return templates.TemplateResponse("index.html",
                                      {"request": request, "products": products, "orders": orders,
                                       "current_user": current_user, "messages": messages})


@order_routes.get("/delete/orders/{order_id}")
def delete_order(request: Request, order_id: int, db: Session = Depends(get_db)):
    order = crud_order.get_order_by_id(order_id=order_id, db=db)
    messages = [
        Message(message=f"You Removed Order from Cart for \"{order.id}\" for \"{order.item_name}\" ", flag="warning")]
    crud_item.update_stock(order_id=order.id, quantity=(-1) * float(order.quantity), db=db)
    crud_order.delete_order(order_id=order_id, db=db)
    products = crud_item.get_items(db)
    token = request.cookies.get("access_token")
    current_user = crud_user.get_current_user(token=token, db=db)
    orders = crud_order.get_orders(db, current_user)
    return templates.TemplateResponse("index.html",
                                      {"request": request, "products": products, "orders": orders,
                                       "current_user": current_user, "messages": messages})
