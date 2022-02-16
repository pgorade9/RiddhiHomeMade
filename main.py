from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
import sqlalchemy
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from passlib.context import CryptContext
from starlette import status

from config import engine
from config import user
from schemas.user import CurrentUser

SECRET = 'your-secret-key'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()


def get_password_hashed(password):
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


manager = LoginManager(SECRET, token_url='/token')

app.mount("/static", StaticFiles(directory="static"), name="static")

from routes import user_routes, item_routes, home_routes

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
        print("results = ", results)
        return result


# the python-multipart package is required to use the OAuth2PasswordRequestForm
@app.post('/token')
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = load_user(email)  # we are using the same function to retrieve the user
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif not verify_password(password, user['password']):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


async def get_current_user(token: str) -> CurrentUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        with engine.connect() as connection:
            print("user = ", user)
            query = sqlalchemy.select(user).where(user.c.name == username)
            results = connection.execute(query).fetchall()
            result = connection.execute(query).first()
    except JWTError:
        raise credentials_exception

    if result is None:
        raise credentials_exception
    return CurrentUser(username=result.name, password=result.email)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt


if __name__ == "__main__":
    uvicorn.run("app", host="127.0.0.1", port="8000")
