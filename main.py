import sqlalchemy
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from config import engine
from config.models import user
from routes import user_routes, item_routes
from routes.home import home_routes

app = FastAPI()

SECRET = 'your-secret-key'

manager = LoginManager(SECRET, token_url='/auth/token')

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_routes)
app.include_router(item_routes)
app.include_router(home_routes)


@manager.user_loader()
def load_user(email: str):  # could also be an asynchronous function
    with engine.connect() as connection:
        print("user = ", user)
        query = sqlalchemy.select(user).where(user.c.email == email)
        results = connection.execute(query).fetchall()
        result = connection.execute(query).first()
        print("results = ",results)
        return result


# the python-multipart package is required to use the OAuth2PasswordRequestForm
@app.post('/auth/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = load_user(email)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
