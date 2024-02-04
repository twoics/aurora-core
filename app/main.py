from fastapi import FastAPI

from app.config.base import init_database
from app.routes.auth import router as auth_router

app = FastAPI()


@app.on_event('startup')
async def start_database():
    await init_database()


app.include_router(auth_router, tags=['Auth'], prefix='/auth')
