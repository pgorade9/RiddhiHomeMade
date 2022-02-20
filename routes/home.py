from fastapi import APIRouter, Request, Form, Depends, Response
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette import status

from config import settings
from config.db import SessionLocal
from schemas import LoginForm
from schemas.forms import RegistrationForm
from utils import crud_user, crud_item
from utils.order import crud_order

home_routes = APIRouter()
templates = Jinja2Templates(directory="templates")


# Dependency
def get_db():
    # print("SessionLocal : ",SessionLocal)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@home_routes.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("gallery.html", {"request": request})


@home_routes.get("/home")
def home(request: Request, db: Session = Depends(get_db)):
    products = crud_item.get_items(db)
    orders = crud_order.get_orders(db)
    token = request.cookies.get("access_token")
    current_user = crud_user.get_current_user(db=db,token=token)
    print("current_user = ",current_user)
    return templates.TemplateResponse("index.html",
                                      {"request": request, "products": products, "orders": orders,"current_user":current_user})


@home_routes.get("/login")
async def login(request: Request):
    form = LoginForm()
    return templates.TemplateResponse("login.html", {"request": request, "form": form})

async def login_form_model(email: str = Form(...), password: str = Form(...)):
    return {'email': email, 'password': password}


@home_routes.post("/login")
async def login(request: Request, form: login_form_model = Depends(), db=Depends(get_db)):

    print("form data= ", form)
    print("email = ", form['email'])
    print("password = ", form['password'])

    email = form['email']
    password = form['password']
    token = crud_user.authenticate_user(db=db, email=email, password=password)
    response = RedirectResponse("/home",status_code=status.HTTP_302_FOUND)
    response.set_cookie("access_token", f"Bearer {token}")
    return response

@home_routes.get("/logout")
async def logout(request: Request):
    pass


@home_routes.get("/invoice")
async def invoice(request: Request):
    pass
#     with engine.connect() as connection:
#         query_user = sqlalchemy.select(user).where(user.c.email == form['email'])
#         fetched_user = connection.execute(query_user).first()
#         query_products = sqlalchemy.select(item)
#         products = connection.execute(query_products).fetchall()
#         if fetched_user is None:
#             return fastapi.responses.RedirectResponse('/register', status_code=status.HTTP_302_FOUND)
#         elif not verify_password(form["password"], fetched_user.password):
#             return fastapi.responses.RedirectResponse('/register', status_code=status.HTTP_302_FOUND)
#         else:
#             data = {"sub": form['email']}
#             token = jwt.encode(data, SECRET, ALGORITHM)
#             print("token : ",token)
#             globals()["current_user"] = CurrentUser(id=fetched_user.id, username=fetched_user.name,
#                                                     email=fetched_user.email)
#             response = templates.TemplateResponse("index.html",
#                                                   {"request": request, "products": products,
#                                                    "current_user": current_user})
#             response.set_cookie("access_token", f"Bearer {token}")
#             return response
#
#
@home_routes.route("/register", methods=['GET', 'POST'])
async def register(request: Request):
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_email(form.email.data):
            print(f'Your Account has been created ! You are now enabled to log in!', 'success')

    return templates.TemplateResponse("register.html", {"request": request, "form": form})

#
# @home_routes.post("/order/{id}")
# async def order(request: Request, id: int):
#     print("order id= ", id)
#
#     with engine.connect() as connection:
#         queryProduct = sqlalchemy.select('item').where(item.c.id == id)
#         product = connection.execute(queryProduct).first()
#
#
#
#         order = Order(name=product.name, price=product.price, total=total, quantity=quantity, user=current_user.id)
