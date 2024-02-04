from fastapi import FastAPI

from app.config.base import init_database
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router

app = FastAPI()


@app.on_event('startup')
async def start_database():
    await init_database()


app.include_router(auth_router, tags=['Auth'], prefix='/auth')
app.include_router(user_router, tags=['User'], prefix='/user')
