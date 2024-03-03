from typing import List

from services.delivery.proto import Delivery
from starlette.websockets import WebSocket


class DataSender:
    def __init__(self, websocket: WebSocket, delivery: Delivery):
        self._ws = websocket
        self._delivery = delivery

    async def send(self, uuid: str, message: List[int]):
        """Send data to specific matrix"""

        await self._delivery.send(uuid, message)
        await self._ws.send_text('DONE')
