from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Session
import models
import schemas
from models import Status, Payment_Status


class CRUD:

    def get_invoices_for_current_user(self, db: Session, current_user: schemas.User):
        return db.query(models.Invoice).filter(models.Invoice.user_id == current_user.id).all()

    def create_invoice(self, db: Session, current_user: schemas.User):
        orders = db.query(models.Order).filter(models.Order.id == current_user.id,
                                               models.Order.status == Status.IN_CART.name)

        sum = 0
        for order in orders:
            sum += float(order.total)
        db_invoice = models.Invoice(user_id=current_user.id, timestamp=datetime.utcnow(), total=sum,
                                    payment_status=Payment_Status.PAID.name)
        db.add(db_invoice)
        db.commit()
        db.refresh(db_invoice)
        return db_invoice


crud_invoice = CRUD()
