from beanie import Document
from beanie import Indexed


class User(Document):
    username: Indexed(str, unique=True)
    password: str
    access_key: str | None = None
    is_admin: bool = False
    is_matrices_access: bool = True

    class Settings:
        name = 'user'
