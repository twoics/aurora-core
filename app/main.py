from fastapi import FastAPI

from app.config.base import init_database

app = FastAPI()


@app.on_event('startup')
async def start_database():
    await init_database()


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/hello/{name}')
async def say_hello(name: str):
    return {'message': f'Hello {name}'}
