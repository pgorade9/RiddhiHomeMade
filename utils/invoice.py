from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import Session
import models
import schemas
from models import Status, Payment_Status


class CRUD:

    def get_invoices_for_current_user(self, db: Session, current_user: schemas.User):
        return db.query(models.Invoice).filter(models.Invoice.user_id == current_user.id).all()

    def get_invoice_unpaid_for_current_user(self, db: Session, current_user: schemas.User):
        return db.query(models.Invoice).filter(models.Invoice.user_id == current_user.id,
                                               models.Invoice.payment_status == Payment_Status.UNPAID.name).first()

    def create_invoice(self, db: Session, current_user: schemas.User):
        orders = db.query(models.Order).filter(models.Order.user_id == current_user.id,
                                               models.Order.status == Status.IN_CART.name).all()

        sum = 0
        print("orders length ========= ", len(orders))
        for order in orders:
            sum += float(order.item_price) * float(order.quantity)
            print(" sum ============ ", sum)
        db_invoice = models.Invoice(user_id=current_user.id, timestamp=datetime.now(), total=sum,
                                    payment_status=Payment_Status.UNPAID.name)
        db.add(db_invoice)
        db.commit()
        db.refresh(db_invoice)
        return db_invoice

    def update_invoice(self, db: Session, current_user: schemas.User):
        orders = db.query(models.Order).filter(models.Order.user_id == current_user.id,
                                               models.Order.status == Status.BILLED.name).all()
        sum = 0
        for order in orders:
            sum += float(order.item_price) * float(order.quantity)
            print("sum_updated ==== ", sum)
        update_data = {"total": sum}
        db.query(models.Invoice).filter(models.Invoice.user_id == current_user.id,
                                        models.payment_status == Payment_Status.UNPAID.name).update(update_data,
                                                                                                    synchronize_session=False)

        db.commit()
        return {"Invoice Updated"}

    def update_delivery_invoice(self, db: Session, invoice_id:int):
        update_data = {"payment_status":Payment_Status.DELIVERED.name}
        db.query(models.Invoice).filter(models.Invoice.id==invoice_id).update(update_data,synchronize_session="evaluate")
        db.commit()
        return {"Invoice Updated as Delivered"}

    def admin_update_payment_invoice(self, db: Session, invoice_id:int):
        update_data = {"payment_status":Payment_Status.PAID.name}
        db.query(models.Invoice).filter(models.Invoice.id==invoice_id).update(update_data,synchronize_session="evaluate")
        db.commit()
        return {"Invoice Updated as PAID"}

    def update_payment_invoice(self, db: Session, current_user: schemas.User):
        update_data = {"payment_status": Payment_Status.PAID.name}
        db.query(models.Invoice).filter(models.Invoice.user_id == current_user.id,
                                        models.Invoice.payment_status == Payment_Status.UNPAID.name).update(update_data,
                                                                                                            synchronize_session="evaluate")
        db.commit()
        return {"Update Payment in Invoice"}

    def delete_invoice(self, db: Session, invoice_id: int):
        result = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
        if result:
            db.delete(result)
            db.commit()
            return result
        return "No Invoice Found to delete"


crud_invoice = CRUD()
