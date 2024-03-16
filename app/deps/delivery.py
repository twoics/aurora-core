from config.redis import get_redis
from fastapi import Depends
from redis.asyncio import Redis as AsyncRedis
from services.delivery.mqtt import MqttDelivery
from services.delivery.proto import Delivery


def get_delivery(redis: AsyncRedis = Depends(get_redis)) -> Delivery:
    """Get object which can send data to matrix"""

    return MqttDelivery(redis)
