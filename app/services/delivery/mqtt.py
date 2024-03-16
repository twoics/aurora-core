import json
import typing

from config.config import Settings
from redis.asyncio import Redis as AsyncRedis
from services.delivery.proto import Delivery


class MqttDelivery(Delivery):
    def __init__(self, redis: AsyncRedis, conf: Settings):
        self._redis = redis
        self._conf = conf

    async def send(self, receiver_uuid: str, message: typing.List[int]):
        to_send = json.dumps({'topic': f'matrix/{receiver_uuid}', 'data': message})
        await self._redis.rpush(self._conf.BROKER_QUEUE_NAME, to_send)
