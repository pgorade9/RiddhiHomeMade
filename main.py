from fastapi import FastAPI,APIRouter
from routes import user_routes,item_routes
app = FastAPI()

app.include_router(user_routes)
app.include_router(item_routes)