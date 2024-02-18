from json import JSONDecodeError
from typing import List

from config.config import Settings
from dependencies.auth import get_user_by_ws
from dependencies.config import get_settings
from dependencies.delivery import get_delivery
from dependencies.pool import get_matrix_connections_pool
from dependencies.preprocess import get_preprocess
from dependencies.repo import get_matrix_repo
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import WebSocket
from fastapi import WebSocketException
from fastapi_limiter.depends import WebSocketRateLimiter
from models import User
from repo.matrix.proto import MatrixRepo
from services.delivery.proto import Delivery
from services.pool.proto import MatrixConnectionsPool
from services.preprocess.proto import Preprocess
from starlette.status import WS_1003_UNSUPPORTED_DATA
from starlette.status import WS_1008_POLICY_VIOLATION
from starlette.status import WS_1009_MESSAGE_TOO_BIG
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


async def preprocess_received_data(handler, data, matrix, user) -> List[int]:
    """Preprocessing of incoming data, preparing it for sending"""

    if not (data_to_send := await handler.handle(data, matrix, user)):
        raise WebSocketException(WS_1009_MESSAGE_TOO_BIG, 'Big message')
    return data_to_send


@router.websocket('/{uuid}')
async def remote_control(
    websocket: WebSocket,
    uuid: str = Path(...),
    config: Settings = Depends(get_settings),
    user: User = Depends(get_user_by_ws),
    matrix_repo: MatrixRepo = Depends(get_matrix_repo),
    preprocess: Preprocess = Depends(get_preprocess),
    delivery: Delivery = Depends(get_delivery),
    pool: MatrixConnectionsPool = Depends(get_matrix_connections_pool),
):
    """Matrix Remote control"""

    if (
        not (matrix := await matrix_repo.get_by_uuid(uuid))
        or not await matrix_repo.user_exists(uuid, user)
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
            ready_data = await preprocess_received_data(preprocess, data, matrix, user)
            await delivery.send(uuid, ready_data)
            await websocket.send_text('DONE')

    except WebSocketDisconnect:
        return
    finally:
        await pool.disconnect(user, matrix)
