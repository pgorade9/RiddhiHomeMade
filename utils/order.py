from sqlalchemy.orm import Session

import models
import schemas
from models import Status


class CRUD:
    def get_orders_incart_for_current_user(self, db: Session, current_user: schemas.User):
        return db.query(models.Order).filter(models.Order.user_id == current_user.id,
                                             models.Order.status == Status.IN_CART.name).all()

    def get_orders_billed_for_current_user(self, db: Session, current_user: schemas.User):
        return db.query(models.Order).filter(models.Order.user_id == current_user.id,
                                             models.Order.status == Status.BILLED.name).all()

    def get_orders_for_current_user(self, db: Session, current_user: schemas.User):
        return db.query(models.Order).filter(models.Order.user_id == current_user.id).all()

    def get_order_by_id(self, db: Session, order_id: int):
        return db.query(models.Order).filter(models.Order.id == order_id).first()

    def get_order_incart_by_item_id(self, db: Session, item_id: int):
        return db.query(models.Order).filter(models.Order.item_id == item_id,
                                             models.Order.status == Status.IN_CART.name).first()

    def update_item_quantity(self, db: Session, item_id: int, quantity: int):
        order = db.query(models.Order).filter(models.Order.item_id == item_id).first()
        update_data = {"quantity": quantity + order.quantity}
        print("updating item found.....", update_data["quantity"])
        result = db.query(models.Order).filter(models.Order.item_id == item_id).update(update_data,
                                                                                       synchronize_session='evaluate')
        if result:
            db.commit()
            return {"Order Updated"}
        return {"Order not found"}

    def get_orders_by_invoice_id(self, db: Session, invoice_id: int):
        return db.query(models.Order).filter(models.Order.invoice_id == invoice_id).all()

    def create_order(self,db: Session,item_id: int, quantity: int, user: schemas.User, invoice_id: int):
        item = db.query(models.Item).filter(models.Item.id == item_id).first()

        if float(item.stock) >= float(quantity):
            print("Item found = ", item)
            # total = float(item.price) * float(quantity)

            db_order = models.Order(item_id=item_id, item_name=item.name, item_price=item.price,
                                    quantity=quantity, user_id=user.id, status=Status.IN_CART.name,
                                    invoice_id=invoice_id)
            print("Entity created")
            db.add(db_order)
            db.commit()
            print("Added and committed")
            db.refresh(db_order)
            print("refresh completed")
            return db_order
        return None

    def delete_order_by_order_id(self, db: Session, order_id: int):
        # order = db.query(models.Order).filter(models.Order.id == order_id).first()
        result = db.query(models.Order).filter(models.Order.id == order_id).delete(synchronize_session=False)
        if result == 1:
            db.commit()
            print("Order deleted from Cart")
            return result
        return {"Order not Found"}

    def update_billed_order(self, db: Session, invoice: schemas.Invoice):
        print("I came to update orders ++++++++++++++++++++")
        update_data = {"invoice_id": invoice.id, "status": Status.BILLED.name}
        db.query(models.Order).filter(models.Order.user_id == invoice.user_id,
                                      models.Order.status == Status.IN_CART.name).update(update_data,
                                                                                      synchronize_session='evaluate')
        db.commit()

    def delete_orders(self, db: Session):
        orders = db.query(models.Order).all()
        if orders:
            for order in orders:
                db.delete(order)
                db.commit()
                print("Order deleted from Cart")
            return {"Deleted all orders "}
        return {"Order not Found"}

    def update_orders_in_unpaid_invoice(self, db: Session, current_user: schemas.User):
        orders = db.query(models.Order).filter(models.Order.user_id == current_user.id,
                                               models.Order.status == Status.IN_CART.name).all()
        existing_orders = db.query(models.Order).filter(models.Order.user_id == current_user.id,
                                                                 models.Order.status == Status.BILLED.name).all()
        for order in orders:
            for existing_order in existing_orders:
                if order.item_id and order.item_id == existing_order.item_id:
                        update_data = {"quantity": existing_order.quantity + order.quantity}
                        db.query(models.Order).filter(models.Order.item_id == order.item_id).update(update_data,
                                                                                                synchronize_session="evaluate")
                        self.delete_order_by_order_id(db=db,order_id=order.id)
        db.commit()
        return {"Orders successfully updated in existing invoice"}
crud_order = CRUD()
