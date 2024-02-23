from pydantic import BaseModel


class AccessKeyGet(BaseModel):
    access_key: str

    class Config:
        json_schema_extra = {
            'example': {
                'access_key': '0c77ea456e9c4abab9289a2c389fd9a5',
            }
        }
