from sqlalchemy.orm import Session

import models
import schemas
from models import Status


class CRUD:
    def get_orders_for_current_user(self, db: Session, current_user: schemas.User):
        return db.query(models.Order).filter(models.Order.user_id == current_user.id).all()

    def get_order_by_id(self, db: Session, order_id: int):
        return db.query(models.Order).filter(models.Order.id == order_id).first()

    def get_orders_by_invoice_id(self, db: Session, invoice_id: int):
        return db.query(models.Order).filter(models.Order.invoice_id == invoice_id).all()

    def create_order(self, item_id: int, quantity: int, user: schemas.User, invoice_id: int, db: Session):
        item = db.query(models.Item).filter(models.Item.id == item_id).first()

        if float(item.stock) >= float(quantity):
            print("Item found = ", item)
            total = float(item.price) * float(quantity)
            db_order = models.Order(item_id=item_id, item_name=item.name, item_price=item.price,
                                    quantity=quantity, total=total, user_id=user.id, status=Status.IN_CART.name,
                                    invoice_id=invoice_id)
            print("Entity created")
            db.add(db_order)
            db.commit()
            print("Added and committed")
            db.refresh(db_order)
            print("refresh completed")
            return db_order
        return None

    def delete_order(self, db: Session, order_id: int):
        # order = db.query(models.Order).filter(models.Order.id == order_id).first()
        result = db.query(models.Order).filter(models.Order.id == order_id).delete(synchronize_session=False)
        if result == 1:
            db.commit()
            print("Order deleted from Cart")
            return result
        return {"Order not Found"}

    def update_invoiced_order(self, db: Session, invoice: schemas.Invoice):
        update_data = {"invoice_id":invoice.id,"status":Status.BILLED.name}
        db.query(models.Order).filter(models.Order.user_id == invoice.user_id).update(update_data,synchronize_session=False)


crud_order = CRUD()
