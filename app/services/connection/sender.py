from typing import List

from services.connection.session import Session
from services.delivery.proto import Delivery
from starlette.websockets import WebSocket


class DataSender:
    def __init__(self, websocket: WebSocket, delivery: Delivery):
        self._ws = websocket
        self._delivery = delivery

    async def send(self, session: Session, message: List[int]):
        """Send data to specific matrix"""

        await self._delivery.send(session.matrix.uuid, message)
        await self._ws.send_text('DONE')
