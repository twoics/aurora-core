from beanie import Document
from beanie import Indexed


class User(Document):
    username: Indexed(str, unique=True)
    password: str
    is_admin: bool = False
    is_banned: bool = False

    class Settings:
        name = 'user'
