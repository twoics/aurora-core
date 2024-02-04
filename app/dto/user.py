from pydantic import BaseModel


class UserRead(BaseModel):
    username: str
    is_admin: bool

    class Config:
        json_schema_extra = {
            'example': {
                'username': 'twoics',
                'is_admin': True,
            }
        }


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            'example': {
                'username': 'twoics',
                'password': 'hello world',
            }
        }


class UserRegister(BaseModel):
    username: str
    password: str

    class Config:
        json_schema_extra = {
            'example': {
                'username': 'twoics',
                'password': 'qwerty',
            }
        }


class UserUpdate(BaseModel):
    username: str

    class Config:
        json_schema_extra = {'example': {'username': 'twoics'}}
