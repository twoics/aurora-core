from typing import List

from beanie import Document
from beanie import Indexed
from beanie import Link
from models.user import User


class Matrix(Document):
    uuid: Indexed(str, unique=True)
    name: str
    is_active: bool = True
    users: List[Link[User]]
    height: int = 16
    width: int = 16

    class Settings:
        name = 'matrix'
