from typing import List

from beanie import Document
from beanie import Indexed
from beanie import Link
from models.user import User
from pydantic import computed_field


class Matrix(Document):
    uuid: Indexed(str, unique=True)
    name: str
    height: int
    width: int

    is_active: bool = True
    users: List[Link[User]]

    @computed_field
    @property
    def resolution(self) -> int:
        return self.height * self.width

    class Settings:
        name = 'matrix'
