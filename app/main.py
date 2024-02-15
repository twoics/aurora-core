import contextlib
import random

import aiomqtt
from config.base import init_database
from dependencies.config import get_settings
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from routes.auth import router as auth_router
from routes.control import router as rc_router
from routes.matrix import router as matrix_router
from routes.user import router as user_router


@contextlib.asynccontextmanager
async def lifespan(*_):
    conf = get_settings()
    await init_database()
    async with aiomqtt.Client(
        conf.MQTT_HOST,
        username=conf.MQTT_USERNAME,
        password=conf.MQTT_PASSWORD,
        identifier=f'aurora-{hex(random.getrandbits(16))}',
    ) as client:
        app.state.amqtt_client = client  # noqa
        yield


app = FastAPI(lifespan=lifespan)
Instrumentator().instrument(app).expose(app)

app.include_router(auth_router, tags=['Auth'], prefix='/auth')
app.include_router(user_router, tags=['User'], prefix='/user')
app.include_router(matrix_router, tags=['Matrix'], prefix='/matrix')
app.include_router(rc_router, tags=['Remote control'], prefix='/remote-control')
