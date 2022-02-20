from sqlalchemy.orm import Session

import models
import schemas
from models import Status


class CRUD:
    def get_orders(self, db: Session):
        return db.query(models.Order).all()

    def get_item_by_id(self, db: Session, order_id: int):
        return db.query(models.Order).filter(models.Order.id == order_id).first()

    def create_order(self,item_id:int,quantity:int,user:schemas.User,db:Session):
        item = db.query(models.Item).filter(models.Item.id == item_id).first()
        total = float(item.price)*float(quantity)
        db_order = models.Order(item_id=item_id,name=item.name,item_price=item.price,
                                quantity=quantity,total=total,user_id=user.id,status=Status.UNPAID)

        db.add(db_order)
        db.commit()
        return item.name

crud_order = CRUD()
