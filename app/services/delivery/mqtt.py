import typing

from aiomqtt import Client
from services.delivery.proto import Delivery


class MqttDelivery(Delivery):
    def __init__(self, client: Client):
        self.client = client

    async def send(self, receiver_uuid: str, message: typing.List[int]):
        pass
        # await self.client.publish(
        #     topic=f'matrix/{receiver_uuid}',  # noqa
        #     payload=bytes(message),
        # )
