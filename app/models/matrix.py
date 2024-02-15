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

    class Settings:
        name = 'matrix'
