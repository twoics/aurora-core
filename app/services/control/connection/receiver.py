from json import JSONDecodeError
from typing import List

from fastapi import WebSocketException
from services.control.connection.session import Session
from services.preprocess.proto import Preprocess
from starlette.status import WS_1003_UNSUPPORTED_DATA
from starlette.status import WS_1009_MESSAGE_TOO_BIG


class DataReceiver:
    def __init__(self, websocket, preprocess: Preprocess, session: Session):
        self._ws = websocket
        self._processor = preprocess
        self._matrix = session.matrix
        self._user = session.user

    async def receive(self) -> List[int]:
        data = await self._receive()
        return await self._preprocess(data)

    async def _receive(self) -> dict:
        """Listen websocket and return incoming message"""

        try:
            return await self._ws.receive_json()
        except JSONDecodeError:
            raise WebSocketException(WS_1003_UNSUPPORTED_DATA, 'Unable parse data')

    async def _preprocess(self, data) -> List[int]:
        """Preprocessing of incoming data, preparing it for sending"""

        if not (
            data_to_send := await self._processor.handle(data, self._matrix, self._user)
        ):
            raise WebSocketException(WS_1009_MESSAGE_TOO_BIG, 'Big message')
        return data_to_send
