import logging
from typing import List

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from config.db import SessionLocal
from models import Message
from routes.home import templates
from utils import crud_user, crud_item, crud_order, crud_invoice

order_routes = APIRouter()
TEMP_INVOICE_ID = 9999


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@order_routes.post("/orders/{item_id}")
async def add_order(request: Request, item_id: int, db: Session = Depends(get_db)):
    logging.info("Adding Order")
    item = crud_item.get_item_by_id(item_id=item_id, db=db)
    form = await request.form()
    quantity = float(form.get("quantity"))
    products = crud_item.get_items(db)
    token = request.cookies.get("access_token")
    if token == "":
        print("I can continue creating session cookies here")
        response = RedirectResponse("/home", status_code=status.HTTP_302_FOUND)
        response.set_cookie("item_id", str(item_id))
        response.set_cookie("quantity", str(quantity))
        return response
    current_user = crud_user.get_current_user(token=token, db=db)

    existing_order = crud_order.get_order_incart_by_item_id(db=db, item_id=item_id)
    if existing_order:
        logging.info("Found Item in Cart. Updating Quantity")
        crud_order.update_item_quantity(db=db,item_id=item_id,quantity=quantity)

    else:
        logging.info("Creating new Order with status In-Cart")
        new_order = crud_order.create_order(db=db, item_id=item_id, quantity=quantity,
                                        user=current_user, invoice_id=TEMP_INVOICE_ID)
        if new_order:
            crud_item.update_stock(order_id=new_order.id, quantity=quantity, db=db)
            orders = crud_order.get_orders_incart_for_current_user(db=db, current_user=current_user)
            messages = [Message(message=f"You Added Product to Cart for \"{new_order.item_name}\" ", flag="success")]
            return templates.TemplateResponse("index.html",
                                          {"request": request, "products": products, "orders": orders,
                                           "current_user": current_user, "messages": messages})
        else:
            orders = crud_order.get_orders_incart_for_current_user(db=db, current_user=current_user)
            messages = [Message(message=f"Item Out of Stock \"{new_order.item_name}\" ", flag="danger")]
            return RedirectResponse(f"/home?messages={messages}&orders={orders}")
    orders = crud_order.get_orders_incart_for_current_user(db=db, current_user=current_user)
    messages = [Message(message=f"Updated item quantity for \"{item.name}\" ", flag="success")]
    return templates.TemplateResponse("index.html",
                                      {"request": request, "products": products, "orders": orders,
                                       "current_user": current_user, "messages": messages})
    # return RedirectResponse(f"/home?messages={messages}&orders={orders}")


@order_routes.get("/remove/orders/{order_id}")
def delete_order(request: Request, order_id: int, db: Session = Depends(get_db)):
    order = crud_order.get_order_by_id(order_id=order_id, db=db)
    messages = [
        Message(message=f"You Removed Order from Cart for \"{order.id}\" for \"{order.item_name}\" ", flag="warning")]
    crud_item.update_stock(order_id=order.id, quantity=(-1) * float(order.quantity), db=db)
    crud_order.delete_order_by_order_id(order_id=order_id, db=db)
    products = crud_item.get_items(db)
    token = request.cookies.get("access_token")
    current_user = crud_user.get_current_user(token=token, db=db)
    orders = crud_order.get_orders_incart_for_current_user(db, current_user)
    return templates.TemplateResponse("index.html",
                                      {"request": request, "products": products, "orders": orders,
                                       "current_user": current_user, "messages": messages})


@order_routes.delete("/delete/order/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    return crud_order.delete_order_by_order_id(db=db, order_id=order_id)


@order_routes.delete("/delete/orders")
def delete_order(db: Session = Depends(get_db)):
    return crud_order.delete_orders(db=db)
