from beanie import Document


class User(Document):
    username: str
    password: str
    is_admin: bool = False

    class Settings:
        name = 'user'
