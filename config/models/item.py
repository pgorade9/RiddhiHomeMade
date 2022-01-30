from sqlalchemy import Table, Column, Integer, String, Float

from config.db import meta

item = Table('item', meta,
             Column('id', Integer, primary_key=True, autoincrement=True),
             Column('name', String(30), nullable=False),
             Column('price', Float),
             Column('stock', Integer, nullable=False),
             Column('image_url', String(30), nullable=False)
             )
