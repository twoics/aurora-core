from pydantic import BaseModel


class CreateClient(BaseModel):
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
