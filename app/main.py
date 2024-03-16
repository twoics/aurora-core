import contextlib

from config.base import init_database
from config.redis import get_redis
from deps.config import get_settings
from fastapi import FastAPI
from fastapi import WebSocketException
from fastapi_limiter import FastAPILimiter
from prometheus_fastapi_instrumentator import Instrumentator
from redis.asyncio import Redis as aredis
from routes.auth import router as auth_router
from routes.control import router as rc_router
from routes.matrix import router as matrix_router
from routes.user import router as user_router
from starlette.status import WS_1013_TRY_AGAIN_LATER


async def websocket_limit_callback(*_):
    """Called when a client sends requests over the limit by websocket"""

    raise WebSocketException(WS_1013_TRY_AGAIN_LATER, 'Too Many Requests')


async def clear_cache():
    """Called when app shutdown for clear all application cache"""

    redis = get_redis()
    conf = get_settings()
    async for key in redis.scan_iter(f'{conf.GLOBAL_CASH_KEY_PREFIX}:*'):
        await redis.delete(key)


@contextlib.asynccontextmanager
async def lifespan(*_):
    conf = get_settings()
    await init_database()
    redis_connection = aredis.from_url(conf.REDIS_URL, encoding='utf8')
    await FastAPILimiter.init(redis_connection, ws_callback=websocket_limit_callback)
    yield


app = FastAPI(lifespan=lifespan)
Instrumentator().instrument(app).expose(app)

app.include_router(auth_router, tags=['Auth'], prefix='/auth')
app.include_router(user_router, tags=['User'], prefix='/user')
app.include_router(matrix_router, tags=['Matrix'], prefix='/matrix')
app.include_router(rc_router, tags=['Remote control'], prefix='/remote-control')
