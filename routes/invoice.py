import logging

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette import status

import schemas
from config.db import SessionLocal
from routes.home import templates
from utils import crud_invoice, crud_user, crud_order
import stripe
from config import settings

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
    unpaid_invoice = crud_invoice.get_invoice_unpaid_for_current_user(db=db, current_user=current_user)
    if unpaid_invoice is None:
        logging.info("Generating new Invoice")
        _ = crud_invoice.create_invoice(db=db, current_user=current_user)
        invoice = schemas.Invoice(id=_.id, user_id=_.user_id, timestamp=_.timestamp, total=_.total,
                                  payment_status=_.payment_status)
        crud_order.update_billed_order(db=db, invoice=invoice)
    else:
        logging.info("Found unpaid Invoice")
        _ = unpaid_invoice
        crud_order.update_orders_in_unpaid_invoice(db, current_user)
        invoice = schemas.Invoice(id=_.id, user_id=_.user_id, timestamp=_.timestamp, total=_.total,
                                  payment_status=_.payment_status)
        crud_order.update_billed_order(db=db, invoice=invoice)
        crud_invoice.update_invoice(db=db, current_user=current_user)

    invoices = crud_invoice.get_invoices_for_current_user(db, current_user)
    orders = crud_order.get_orders_for_current_user(db, current_user)
    return templates.TemplateResponse("invoice.html",
                                      {"request": request, "current_user": current_user,
                                       "orders": orders, "invoices": invoices, "pub_key": settings.PUB_KEY})


@invoice_routes.get("/invoice")
async def invoice(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    current_user = crud_user.get_current_user(token=token, db=db)
    orders = crud_order.get_orders_for_current_user(db, current_user)

    invoices = crud_invoice.get_invoices_for_current_user(db, current_user)
    return templates.TemplateResponse("invoice.html",
                                      {"request": request, "current_user": current_user,
                                       "orders": orders, "invoices": invoices, "pub_key": settings.PUB_KEY})


@invoice_routes.post("/pay/{invoice_id}/{amt}")
async def pay(request: Request, invoice_id: int, amt: float, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    current_user = crud_user.get_current_user(token=token, db=db)
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
    crud_invoice.update_payment_invoice(db=db, current_user=current_user)
    return RedirectResponse("/invoice", status_code=status.HTTP_302_FOUND)


@invoice_routes.delete("/delete/invoice/{invoice_id}")
def delete_user(invoice_id: int, db: Session = Depends(get_db)):
    return crud_invoice.delete_invoice(db=db, invoice_id=invoice_id)

@invoice_routes.post("/update_payment/invoice/{invoice_id}")
def update_invoice(invoice_id: int, db: Session = Depends(get_db)):
    return crud_invoice.admin_update_payment_invoice(db=db, invoice_id=invoice_id)

@invoice_routes.post("/update_delivery/invoice/{invoice_id}")
def update_invoice(invoice_id: int, db: Session = Depends(get_db)):
    return crud_invoice.update_delivery_invoice(db=db, invoice_id=invoice_id)
