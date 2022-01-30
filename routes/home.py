import sqlalchemy
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config import engine, item

home_routes = APIRouter()
templates = Jinja2Templates(directory="templates")


@home_routes.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("gallery.html", {"request": request})


@home_routes.get("/home", response_class=HTMLResponse)
def home(request: Request):
    with engine.connect() as connection:
        query = sqlalchemy.select([item])
        results = connection.execute(query).fetchall()
    # return results
    return templates.TemplateResponse("index.html", {"request": request, "products": results})
