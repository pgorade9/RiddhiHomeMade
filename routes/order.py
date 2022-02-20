from fastapi import APIRouter, Depends, Form, Request,status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from config.db import SessionLocal
from routes.home import templates
from utils import crud_user, crud_item
from utils.order import crud_order

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
async def add_order(request: Request, item_id:int, db: Session = Depends(get_db)):
    form = await request.form()
    quantity = form.get("quantity")
    print("quantity = ",quantity )
    products = crud_item.get_items(db)
    orders = crud_order.get_orders(db)
    token = request.cookies.get("access_token")
    current_user = crud_user.get_current_user(token = token,db=db)
    item_name = crud_order.create_order(db=db,item_id=item_id,quantity=quantity,user=current_user)
    messages = [f"You Ordered Product \"{item_name}\""]
    return templates.TemplateResponse("index.html",
                                      {"request": request, "products": products, "orders": orders,
                                       "current_user": current_user,"messages":messages})

