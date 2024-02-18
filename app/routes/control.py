from json import JSONDecodeError

from config.config import Settings
from dependencies.auth import get_user_by_ws
from dependencies.config import get_settings
from dependencies.delivery import get_delivery
from dependencies.handlers import get_stream_handler
from dependencies.pool import get_matrix_connections_pool
from dependencies.repo import matrix_repo
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import WebSocket
from fastapi import WebSocketException
from fastapi_limiter.depends import WebSocketRateLimiter
from models import User
from repo.matrix.proto import MatrixRepo
from services.delivery.proto import Delivery
from services.handler.proto import StreamHandler
from services.pool.proto import MatrixConnectionsPoolProto
from starlette.status import WS_1003_UNSUPPORTED_DATA
from starlette.status import WS_1008_POLICY_VIOLATION
from starlette.websockets import WebSocketDisconnect

router = APIRouter()


async def receive(websocket) -> dict:
    """Listen websocket and return incoming message"""

    try:
        return await websocket.receive_json()
    except JSONDecodeError:
        raise WebSocketException(WS_1003_UNSUPPORTED_DATA, 'Unable parse data')


async def validate_client_permissions(websocket, user, matrix, ratelimit, pool) -> None:
    """Check client permissions and raise ws exception if something wrong"""

    await ratelimit(websocket, context_key=f'{user.id}:{matrix.uuid}')
    if not await pool.is_connected(user, matrix):
        raise WebSocketException(WS_1008_POLICY_VIOLATION, 'Access denied')


@router.websocket('/{uuid}')
async def remote_control(
    websocket: WebSocket,
    uuid: str = Path(...),
    config: Settings = Depends(get_settings),
    user: User = Depends(get_user_by_ws),
    repo: MatrixRepo = Depends(matrix_repo),
    handler: StreamHandler = Depends(get_stream_handler),
    delivery: Delivery = Depends(get_delivery),
    pool: MatrixConnectionsPoolProto = Depends(get_matrix_connections_pool),
):
    """Matrix Remote control"""

    if (
        not (matrix := await repo.get_by_uuid(uuid))
        or not await repo.user_exists(uuid, user)
        or not user.is_matrices_access
    ):
        raise WebSocketException(WS_1003_UNSUPPORTED_DATA, 'Unsupported UUID')

    await websocket.accept()
    ratelimit = WebSocketRateLimiter(seconds=1, times=config.WS_QUERY_COUNT_PER_SECOND)
    await pool.connect(user, matrix)

    try:
        while True:
            data = await receive(websocket)
            await validate_client_permissions(websocket, user, matrix, ratelimit, pool)
            data_to_send = await handler.handle(data, uuid, user)
            await delivery.send(uuid, data_to_send)
            await websocket.send_text('DONE')

    except WebSocketDisconnect:
        return
    finally:
        await pool.disconnect(user, matrix)
