from sqlalchemy import create_engine,MetaData,Table,Column,Integer,String

engine = create_engine("mysql+mysqldb://root:ganapati@localhost:3306/friends")

meta = MetaData()

# from sqlalchemy import text
# with engine.connect() as connection:
#     result = connection.execute(text("select * from friend"))
#     for row in result:
#         print("username:", row['first_name'])


