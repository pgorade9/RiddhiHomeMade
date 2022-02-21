from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Session
import models
from models import Status


class CRUD:
    def get_orders_by_invoice_id(self, db: Session, invoice_id: int):
        return db.query(models.Order).filter(models.Order.invoice_id == invoice_id).all()

    def get_orders_for_current_user(self, db: Session, current_user_id: int):
        return db.query(models.Order) \
            .filter(models.Order.user_id == current_user_id) \
            .filter(models.Order.status == Status.UNPAID.name).all()

    def get_invoices_for_current_user(self, db: Session, current_user_id: int):
        return db.query(models.Invoice).filter(models.Invoice.user_id == current_user_id).all()

    def create_invoice(self, db: Session, current_user_id: int):
        orders = db.query(models.Order).filter(models.Order.id == current_user_id).all()
        sum = 0
        for order in orders:
            sum += order.total
        db_invoice = models.Invoice(user_id=current_user_id, timestamp=datetime.utcnow(), total=sum,
                                    status=Status.PAID.name)
        db.add(db_invoice)
        db.commit()
        db.refresh(db_invoice)



crud_invoice = CRUD()
