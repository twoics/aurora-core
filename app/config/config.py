from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # database configurations
    DATABASE_URL: str

    class Config:
        env_file = '.env'
