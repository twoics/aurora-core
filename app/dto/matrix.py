from typing import List

from dto.user import UserRead
from pydantic import BaseModel


class MatrixCreate(BaseModel):
    uuid: str
    name: str
    width: int = 16
    height: int = 16

    class Config:
        json_schema_extra = {
            'example': {
                'uuid': '0SN91roa6',
                'name': 'aurora',
                'width': 16,
                'height': 16,
            }
        }


class MatrixUpdate(MatrixCreate):
    pass


class MatrixGet(BaseModel):
    uuid: str
    name: str
    width: int
    height: int

    class Config:
        json_schema_extra = {
            'example': {
                'uuid': '0SN91roa6',
                'name': 'aurora',
                'width': 16,
                'height': 16,
            }
        }


class MatrixDetailGet(BaseModel):
    uuid: str
    name: str
    width: int
    height: int
    users: List[UserRead]

    class Config:
        json_schema_extra = {
            'example': {
                'uuid': '0SN91roa6',
                'name': 'aurora',
                'width': 16,
                'height': 16,
                'users': [
                    {
                        'username': 'twoics',
                        'is_admin': True,
                    },
                    {
                        'username': 'amogus',
                        'is_admin': False,
                    },
                ],
            }
        }
