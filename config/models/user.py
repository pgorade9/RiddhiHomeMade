from sqlalchemy import Table,Column,Integer,String

from config.db import meta

user = Table('user', meta,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String(16), nullable=False),
    Column('email_address', String(60)),
    Column('nickname', String(50), nullable=False)
)