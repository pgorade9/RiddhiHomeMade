from sqlalchemy import Table, Column, Integer, String, ForeignKey

from config.db import meta

user = Table('order', meta,
             Column('id', Integer, primary_key=True, autoincrement=True),
             Column('user', Integer, ForeignKey('user.id')),
             Column('email', String(60)),
             Column('nick_name', String(30), nullable=False),
             Column('image_url', String(30), nullable=False)
             )
