from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette import status

from config.db import SessionLocal
from routes.home import templates
from utils import crud_invoice, crud_user
import stripe

invoice_routes = APIRouter()


# Dependency
def get_db():
    print("SessionLocal : ", SessionLocal)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@invoice_routes.post("/invoice")
async def invoice(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    current_user = crud_user.get_current_user(token=token, db=db)
    orders = crud_invoice.get_orders_for_current_user(db, current_user.id)
    crud_invoice.create_invoice(db=db, current_user_id=current_user.id)
    invoices = crud_invoice.get_invoices_for_current_user(db, current_user.id)
    for order in orders:
        print("order : ", order)
    return templates.TemplateResponse("invoice.html",
                                      {"request": request, "current_user": current_user,
                                       "orders": orders, "invoices": invoices})


@invoice_routes.post("/pay/{invoice_id}/{amt}")
async def pay(request: Request, invoice_id: int, amt: float):
    print(request.form)
    form = await request.form()
    email = form.get("stripeEmail")
    source = form.get("stripeToken")
    customer = stripe.Customer.create(email=email, source=source)
    amt = int(amt)
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amt,
        currency='usd',
        description="The Product"
    )
    return RedirectResponse("/invoice", status_code=status.HTTP_302_FOUND)
