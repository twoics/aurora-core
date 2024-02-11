import contextlib
import random

import aiomqtt
from fastapi import FastAPI

from app.config.base import init_database
from app.dependencies.config import get_settings
from app.routes.auth import router as auth_router
from app.routes.control import router as rc_router
from app.routes.matrix import router as matrix_router
from app.routes.user import router as user_router


@contextlib.asynccontextmanager
async def aiomqtt_lifespan(*_):
    conf = get_settings()
    async with aiomqtt.Client(
        conf.MQTT_HOST,
        username=conf.MQTT_USERNAME,
        password=conf.MQTT_PASSWORD,
        identifier=f'aurora-{hex(random.getrandbits(16))}',
    ) as client:
        app.state.amqtt_client = client  # noqa
        yield


app = FastAPI(lifespan=aiomqtt_lifespan)


@app.on_event('startup')
async def start_database():
    await init_database()


app.include_router(auth_router, tags=['Auth'], prefix='/auth')
app.include_router(user_router, tags=['User'], prefix='/user')
app.include_router(matrix_router, tags=['Matrix'], prefix='/matrix')
app.include_router(rc_router, tags=['Remote control'], prefix='/remote-control')
