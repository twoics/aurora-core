from json import JSONDecodeError

from config.config import Settings
from dependencies.auth import get_user_by_ws
from dependencies.config import get_settings
from dependencies.delivery import get_delivery
from dependencies.handlers import get_stream_handler
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
from starlette.status import WS_1003_UNSUPPORTED_DATA
from starlette.websockets import WebSocketDisconnect

router = APIRouter()


@router.websocket('/{uuid}')
async def remote_control(
    websocket: WebSocket,
    uuid: str = Path(...),
    config: Settings = Depends(get_settings),
    user: User = Depends(get_user_by_ws),
    repo: MatrixRepo = Depends(matrix_repo),
    handler: StreamHandler = Depends(get_stream_handler),
    delivery: Delivery = Depends(get_delivery),
):
    """Matrix Remote control"""

    if not await repo.get_by_uuid(uuid) or not await repo.user_exists(uuid, user):
        raise WebSocketException(WS_1003_UNSUPPORTED_DATA, 'Unsupported UUID')

    await websocket.accept()
    ratelimit = WebSocketRateLimiter(seconds=1, times=config.WS_QUERY_COUNT_PER_SECOND)
    while True:
        try:
            data = await websocket.receive_json()
        except JSONDecodeError:
            raise WebSocketException(WS_1003_UNSUPPORTED_DATA, 'Unable parse data')
        except WebSocketDisconnect:
            return

        await ratelimit(websocket, context_key=data)
        data_to_send = await handler.handle(data, uuid, user)
        await delivery.send(uuid, data_to_send)
        await websocket.send_text('DONE')
