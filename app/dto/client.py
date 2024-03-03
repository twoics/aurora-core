from pydantic import BaseModel


class ClientCreate(BaseModel):
    name: str
    description: str = ''

    class Config:
        json_schema_extra = {
            'example': {
                'name': 'tg-bot',
                'description': 'Telegram bot client',
            }
        }


class ClientGet(BaseModel):
    name: str
    description: str

    class Config:
        json_schema_extra = {
            'example': {
                'name': 'tg-bot',
                'description': 'Telegram bot client',
            }
        }


class ClientAccessKeyGet(BaseModel):
    access_key: str

    class Config:
        json_schema_extra = {
            'example': {
                'access_key': '1aee1c2c8fab427493182323de42bf48',
            }
        }
