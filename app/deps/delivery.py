from config.config import Settings
from config.redis import get_redis
from deps.config import get_settings
from fastapi import Depends
from redis.asyncio import Redis as AsyncRedis
from services.delivery.mqtt import TaskQueueDelivery
from services.delivery.proto import Delivery


def get_delivery(
    redis: AsyncRedis = Depends(get_redis), config: Settings = Depends(get_settings)
) -> Delivery:
    """Get object which can send data to matrix"""

    return TaskQueueDelivery(redis, config)
