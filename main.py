import stripe
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config import Base, engine, settings
from routes import user_routes, home_routes, item_routes, order_routes, invoice_routes

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(user_routes)
app.include_router(item_routes)
app.include_router(home_routes)
app.include_router(order_routes)
app.include_router(invoice_routes)
stripe.api_key = settings.SECRET_KEY

