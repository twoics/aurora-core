from typing import List

from dto.user import UserRead
from pydantic import BaseModel


class MatrixCreate(BaseModel):
    uuid: str
    name: str

    class Config:
        json_schema_extra = {'example': {'uuid': '0SN91roa6', 'name': 'first-matrix'}}


class MatrixUpdate(MatrixCreate):
    pass


class MatrixGet(BaseModel):
    uuid: str
    name: str

    class Config:
        json_schema_extra = {'example': {'uuid': '0SN91roa6', 'name': 'aurora'}}


class MatrixDetailGet(BaseModel):
    uuid: str
    name: str
    users: List[UserRead]

    class Config:
        json_schema_extra = {
            'example': {
                'uuid': '0SN91roa6',
                'name': 'first-matrix',
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
