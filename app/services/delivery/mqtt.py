import typing

from aiomqtt import Client

from app.services.delivery.proto import Delivery


class MqttDelivery(Delivery):
    def __init__(self, client: Client):
        self.client = client

    async def send(self, to: str, message: typing.List[int]):
        await self.client.publish(topic=to, payload=bytes(message))  # noqa
