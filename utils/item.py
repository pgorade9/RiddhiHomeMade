from sqlalchemy.orm import Session

import models
import schemas


class CRUD:
    def get_items(self, db: Session):
        return db.query(models.Item).all()

    def get_item_by_id(self, db: Session, item_id: int):
        return db.query(models.Item).filter(models.Item.id == item_id).first()

    def create_item(self, item: schemas.Item, db: Session):
        item_db = models.Item(name=item.name, price=item.price, stock=item.stock, image_url=item.image_url)
        db.add(item_db)
        db.commit()
        db.refresh(item_db)
        return db.query(models.Item).filter(models.Item.name == item.name).first()

    def delete_item(self, db: Session, item_id: int):
        result = db.query(models.Item).filter(models.Item.id == item_id).delete(synchronize_session=False)
        db.commit()
        return db.query(models.Item).all()

    def update_item(self, item: schemas.Item, db: Session, ):
        update_data = {}
        update_data["stock"] = item.stock
        update_data["description"] = item.description
        update_data["price"] = item.price

        result = db.query(models.Item).filter(models.Item.id == item.id).update(update_data, synchronize_session=False)
        if result == 1:
            print("result = ", result)
            db.commit()
            return db.query(models.Item).all()
        return {"No Item Found to Update"}

    def update_stock(self, order_id: int, quantity: int, db: Session):
        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        item = db.query(models.Item).filter(models.Item.id == order.item_id).first()
        current_stock = item.stock
        updated_stock = {"stock": current_stock - quantity}

        result = db.query(models.Item).filter(models.Item.id == item.id).update(updated_stock,
                                                                                synchronize_session=False)
        if result == 1:
            print("result = ", result)
            db.commit()
            return db.query(models.Item).all()
        return {"No Item Found to Update"}


crud_item = CRUD()
