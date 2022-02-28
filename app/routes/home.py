from typing import List

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette import status
import logging
from app import schemas
from app.config import SessionLocal
from app.models import Message
from app.schemas import LoginForm
from app.schemas.forms import RegistrationForm
from app.utils import crud_user, crud_item
from app.utils.order import crud_order

home_routes = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# Dependency
def get_db():
    # print("SessionLocal : ",SessionLocal)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@home_routes.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    if request.cookies.get("access_token"):
        token = request.cookies.get("access_token")
        try:
            current_user = crud_user.get_current_user(db=db, token=token)
        except Exception as ex:
            response = templates.TemplateResponse("gallery.html", {"request": request})
            response.set_cookie("access_token", "")
            return response
        return templates.TemplateResponse("gallery.html", {"request": request, "current_user": current_user})
    return templates.TemplateResponse("gallery.html", {"request": request})


@home_routes.get("/home")
def home(request: Request, messages: List[Message] = None, orders: List[schemas.Order] = None,
         db: Session = Depends(get_db)):
    products = crud_item.get_items(db)

    if request.cookies.get("access_token"):
        token = request.cookies.get("access_token")
        current_user = crud_user.get_current_user(db=db, token=token)
        logging.info("Current User : " + current_user.name)
        orders = crud_order.get_orders_incart_for_current_user(db, current_user)
        return templates.TemplateResponse("index.html",
                                          {"request": request, "products": products, "orders": orders,
                                           "current_user": current_user, "messages": messages})
    return templates.TemplateResponse("index.html",
                                      {"request": request, "products": products, "messages": messages})


@home_routes.get("/login")
async def login(request: Request):
    form = LoginForm()
    return templates.TemplateResponse("login.html", {"request": request, "form": form})


async def login_form_model(email: str = Form(...), password: str = Form(...)):
    return {'email': email, 'password': password}


@home_routes.post("/login")
async def login(request: Request, form: login_form_model = Depends(), db=Depends(get_db)):
    form = await request.form()
    email = form['email']
    password = form['password']
    token = crud_user.authenticate_user(db=db, email=email, password=password)
    response = RedirectResponse("/home", status_code=status.HTTP_302_FOUND)
    response.set_cookie("access_token", f"Bearer {token}")
    return response


@home_routes.get("/logout")
async def logout(request: Request):
    response = RedirectResponse("/login", status_code=status.HTTP_302_FOUND)
    response.set_cookie("access_token", "")
    return response


@home_routes.get("/register")
async def register(request: Request):
    form = RegistrationForm()
    return templates.TemplateResponse("register.html", {"request": request, "form": form})


@home_routes.post("/register")
async def register(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    try:
        current_user = crud_user.register_user(db=db, form=form)
    except Exception as ex:
        messages = [
            Message(message=f"Email already taken = \"{form.get('email')}\". Please try another  ", flag="danger")]
        form = RegistrationForm()
        response = templates.TemplateResponse("register.html", {"request": request, "form": form, "messages": messages})
        return response
    token = crud_user.get_token(email=current_user.email)
    messages = [
        Message(message=f"Registration Successful !! ", flag="success")]
    products = crud_item.get_items(db)
    response = templates.TemplateResponse("index.html",
                                          {"request": request, "current_user": current_user, "products": products,
                                           "messages": messages})
    response.set_cookie("access_token", f"Bearer {token}")
    return response
