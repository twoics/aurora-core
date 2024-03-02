from beanie import Document


class Client(Document):
    name: str
    description: str
    access_key: str

    class Settings:
        name = 'client'
