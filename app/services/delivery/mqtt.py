import json
import typing

from redis.asyncio import Redis as AsyncRedis
from services.delivery.proto import Delivery


class MqttDelivery(Delivery):
    def __init__(self, redis: AsyncRedis):
        self._redis = redis

    async def send(self, receiver_uuid: str, message: typing.List[int]):
        to_send = json.dumps({'topic': f'matrix/{receiver_uuid}', 'data': message})
        await self._redis.rpush(to_send)
