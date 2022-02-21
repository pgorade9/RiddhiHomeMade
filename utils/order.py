from sqlalchemy.orm import Session

import models
import schemas
from models import Status


class CRUD:
    def get_orders(self, db: Session,user: schemas.User):
        return db.query(models.Order).filter(models.Order.user_id == user.id).all()

    def get_order_by_id(self, db: Session, order_id: int):
        return db.query(models.Order).filter(models.Order.id == order_id).first()

    def create_order(self, item_id: int, quantity: int, user: schemas.User, db: Session):
        item = db.query(models.Item).filter(models.Item.id == item_id).first()

        if float(item.stock) >= float(quantity):
            print("Item found = ", item)
            total = float(item.price) * float(quantity)
            db_order = models.Order(item_id=item_id, item_name=item.name, item_price=item.price,
                                    quantity=quantity, total=total, user_id=user.id, status=Status.UNPAID.name)
            print("Entity created")
            db.add(db_order)
            db.commit()
            print("Added and committed")
            db.refresh(db_order)
            print("refresh completed")
            return db_order
        return None

    def delete_order(self, db: Session, order_id: int):
        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        result = db.query(models.Order).filter(models.Order.id == order_id).delete(synchronize_session=False)
        if result == 1:
            db.commit()
            print("Order deleted from Cart")
            return result
        return {"Order not Found"}


crud_order = CRUD()
