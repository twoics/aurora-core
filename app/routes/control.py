import logging
from json import JSONDecodeError
from typing import List

from config.config import Settings
from deps.auth import get_user_by_ws
from deps.config import get_settings
from deps.delivery import get_delivery
from deps.pool import get_matrix_connections_pool
from deps.preprocess import get_preprocess
from deps.repo import get_matrix_repo
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
logger = logging.getLogger(__name__)


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


async def validate_credentials(matrix_repo: MatrixRepo, user: User, uuid: str):
    """Validate user access to current matrix"""

    if (
        not await matrix_repo.get_by_uuid(uuid)
        or not await matrix_repo.user_exists(uuid, user)
        or not user.is_matrices_access
    ):
        logger.info(f'User {user.username} does not have access connect to the matrix')
        raise WebSocketException(WS_1003_UNSUPPORTED_DATA, 'Unsupported UUID')


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

    logger.info(f'User {user.username} initiate connect to matrix {uuid}')
    await validate_credentials(matrix_repo, user, uuid)
    await websocket.accept()
    logger.info('Connection accepted')

    matrix = await matrix_repo.get_by_uuid(uuid)
    ratelimit = WebSocketRateLimiter(seconds=1, times=config.WS_QUERY_COUNT_PER_SECOND)
    await pool.connect(user, matrix)
    logger.info(f'Put {user.username}:{matrix.uuid} connection to pool')

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
        logger.info(f'Delete {user.username}:{matrix.uuid} connection from pool')
        logger.info('Connection closed')
