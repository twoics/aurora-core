from json import JSONDecodeError

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import WebSocket
from fastapi import WebSocketException
from starlette.status import WS_1003_UNSUPPORTED_DATA
from starlette.websockets import WebSocketDisconnect

from app.dependencies.handlers import get_stream_handler
from app.dependencies.repo import matrix_repo
from app.repo.matrix.proto import MatrixRepo
from app.services.handler.proto import StreamHandler

router = APIRouter()


@router.websocket('/{uuid}/rgb')
async def remote_control(
    websocket: WebSocket,
    uuid: str = Path(...),
    repo: MatrixRepo = Depends(matrix_repo),
    handler: StreamHandler = Depends(get_stream_handler),
):
    if not await repo.get_by_uuid(uuid):
        raise WebSocketException(WS_1003_UNSUPPORTED_DATA, 'UUID does not exist')

    await websocket.accept()
    while True:
        try:
            try:
                data = await websocket.receive_json()
                _ = data
            except JSONDecodeError:
                raise WebSocketException(WS_1003_UNSUPPORTED_DATA, 'Unable parse data')
            # data_to_send = await handler.handle(data, uuid, '')
        except WebSocketDisconnect:
            return
        await websocket.send_text('DONE')
