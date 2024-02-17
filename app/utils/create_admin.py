from config.base import init_database
from models import User
from services.auth.credentials import get_password_hash


async def create_admin(username: str, password: str):
    """Creates a new admin with given credentials"""

    await init_database()
    admin = User(username=username, password=get_password_hash(password), is_admin=True)
    await admin.insert()
