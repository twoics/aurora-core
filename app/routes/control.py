from json import JSONDecodeError

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import WebSocket
from fastapi import WebSocketException
from starlette.status import WS_1003_UNSUPPORTED_DATA
from starlette.websockets import WebSocketDisconnect

from app.dependencies.delivery import get_delivery
from app.dependencies.handlers import get_stream_handler
from app.dependencies.repo import matrix_repo
from app.repo.matrix.proto import MatrixRepo
from app.services.delivery.proto import Delivery
from app.services.handler.proto import StreamHandler

router = APIRouter()


@router.websocket('/{uuid}')
async def remote_control(
    websocket: WebSocket,
    uuid: str = Path(...),
    repo: MatrixRepo = Depends(matrix_repo),
    handler: StreamHandler = Depends(get_stream_handler),
    delivery: Delivery = Depends(get_delivery),
):
    """Matrix Remote control"""

    if not await repo.get_by_uuid(uuid):
        raise WebSocketException(WS_1003_UNSUPPORTED_DATA, 'UUID does not exist')

    await websocket.accept()
    while True:
        try:
            try:
                data = await websocket.receive_json()
            except JSONDecodeError:
                raise WebSocketException(WS_1003_UNSUPPORTED_DATA, 'Unable parse data')
            data_to_send = await handler.handle(data, uuid, '')
            await delivery.send(uuid, data_to_send)
        except WebSocketDisconnect:
            return
        await websocket.send_text('DONE')
