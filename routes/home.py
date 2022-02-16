import fastapi
import sqlalchemy
import starlette.status as status
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext

from config import engine, item, user
from main import manager
from schemas import LoginForm
from schemas.forms import RegistrationForm
from schemas.user import CurrentUser

home_routes = APIRouter()
templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@home_routes.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("gallery.html", {"request": request})


@home_routes.get("/home")
def home(request: Request):
    with engine.connect() as connection:
        query = sqlalchemy.select([item])
        results = connection.execute(query).fetchall()
    # return results
    return templates.TemplateResponse("index.html",
                                      {"request": request, "products": results})


@home_routes.get("/login")
async def login(request: Request):
    form = LoginForm()
    return templates.TemplateResponse("login.html", {"request": request, "form": form})


@home_routes.get("/logout")
async def logout(request: Request):
    pass


@home_routes.get("/invoice")
async def invoice(request: Request):
    pass


async def login_form_model(email: str = Form(...), password: str = Form(...)):
    return {'email': email, 'password': password}


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


@home_routes.post("/login")
async def login(request: Request, form: login_form_model = Depends()):
    print("form data= ", form)
    print("email = ", form['email'])
    print("password = ", form['password'])
    with engine.connect() as connection:
        query_user = sqlalchemy.select(user).where(user.c.email == form['email'])
        fetched_user = connection.execute(query_user).first()
        query_products = sqlalchemy.select(item)
        products = connection.execute(query_products).fetchall()
        if fetched_user is None:
            return fastapi.responses.RedirectResponse('/register', status_code=status.HTTP_302_FOUND)
        elif not verify_password(form["password"],fetched_user.password):
            return fastapi.responses.RedirectResponse('/register', status_code=status.HTTP_302_FOUND)
        else:
            current_user = CurrentUser(username=fetched_user.name, email=fetched_user.email)
            return templates.TemplateResponse("index.html",
                                              {"request": request, "products": products, "current_user": current_user})


@home_routes.route("/register", methods=['GET', 'POST'])
async def register(request: Request):
    form = RegistrationForm()

    if request.method == 'POST':
        if form.validate_email(form.email.data):
            print(f'Your Account has been created ! You are now enabled to log in!', 'success')

    return templates.TemplateResponse("register.html", {"request": request, "form": form})
