from starlette.status import WS_1013_TRY_AGAIN_LATER
from websockets import WebSocketException


async def websocket_limit_callback(*_):
    """Called when a client sends requests over the limit by websocket"""

    raise WebSocketException(WS_1013_TRY_AGAIN_LATER, 'Too Many Requests')
