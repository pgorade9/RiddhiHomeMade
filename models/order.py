from sqlalchemy import Table, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationships
from config.db import meta

user = Table('order', meta,
             Column('id', Integer, primary_key=True, autoincrement=True),
             Column('user', Integer, ForeignKey('user.id'),nullable=False),
             Column('quantity',Integer, nullable=False),
             Column('price',Float,nullable=False),
             Column('total',Float,nullable=False),
             Column('invoice_id',Integer,ForeignKey('invoice.id'))
             )
