from functools import lru_cache

from pydantic_settings import BaseSettings


@lru_cache
class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    HASH_SALT: str
    TIME_ZONE: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    WS_QUERY_COUNT_PER_SECOND: int
    GLOBAL_CASH_KEY_PREFIX: str

    class Config:
        env_file = '.env'
