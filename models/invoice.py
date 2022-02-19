from sqlalchemy import Table, Column, Integer, String, ForeignKey, Float, DateTime

from config.db import meta

user = Table('invoice', meta,
             Column('id', Integer, primary_key=True, autoincrement=True),
             Column('user', Integer, ForeignKey('user.id'),nullable=False),
             Column('timestamp',DateTime, nullable=False),
             Column('total',Float,nullable=False),
             Column('orders',Float,nullable=False),
             Column('payment_status',String,nullable=False),
             Column('order_status',String,nullable=False)
             )
