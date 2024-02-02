from beanie import Document


class User(Document):
    username: str
    password: str
    is_admin: bool

    class Settings:
        name = 'user'
