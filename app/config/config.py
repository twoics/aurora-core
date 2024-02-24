from functools import lru_cache

from pydantic_settings import BaseSettings


@lru_cache
class Settings(BaseSettings):
    DATABASE_URL: str = 'mongodb://admin:admin@localhost:27017/matrix?authSource=admin'
    REDIS_URL: str = 'redis://localhost:6379'
    SECRET_KEY: str = 'secret'
    ALGORITHM: str = 'HS256'
    HASH_SALT: str = 'YJZr3Pqf89R1sG6jIyvC5.'
    TIME_ZONE: str = 'Asia/Krasnoyarsk'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 180
    MQTT_HOST: str = 'localhost'
    MQTT_PORT: int = 1883
    MQTT_USERNAME: str = 'twoics'
    MQTT_PASSWORD: str = 'main'
    WS_QUERY_COUNT_PER_SECOND: int = 60
    GLOBAL_CASH_KEY_PREFIX: str = 'aurora'

    # class Config:
    #     env_file = '.env'
