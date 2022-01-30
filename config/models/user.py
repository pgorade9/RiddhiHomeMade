from sqlalchemy import Table, Column, Integer, String

from config.db import meta

user = Table('user', meta,
             Column('id', Integer, primary_key=True, autoincrement=True),
             Column('name', String(30), nullable=False),
             Column('password', String(30), nullable=False),
             Column('email', String(60)),
             Column('nick_name', String(30), nullable=True),
             Column('image_url', String(30), nullable=True)
             )
