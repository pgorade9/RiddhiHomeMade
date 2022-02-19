from fastapi import FastAPI

from config import Base, engine
from routes import user_routes, home_routes


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(user_routes)
app.include_router(home_routes)

