from typing import List
from typing import Optional

from beanie import Document
from beanie import Link

from app.models.user import User


class Matrix(Document):
    uuid: str
    name: str
    is_active: bool = True
    users: Optional[List[Link[User]]] = None

    class Settings:
        name = 'matrix'
