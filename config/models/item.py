from sqlalchemy import Table,Column,Integer,String,Float

from config.db import meta

item = Table('item', meta,
    Column('item_id', Integer, primary_key=True),
    Column('item_name', String(20), nullable=False),
    Column('item_price', Float),
    Column('item_stock', Integer, nullable=False),
    Column('item_image_url', String(30), nullable=False)
)