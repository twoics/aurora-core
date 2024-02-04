from bson import ObjectId

from app.dto.user import UserRegister
from app.models import User
from app.services.auth.credentials import get_password_hash


class UserRepository:
    @classmethod
    async def get_by_name(cls, username: str) -> User | None:
        return await User.find_one(User.username == username)

    @classmethod
    async def create_user(cls, user: UserRegister):
        data = user.model_dump()
        data['password'] = get_password_hash(data['password'])
        await User(**data).insert()

    @classmethod
    async def get_by_id(cls, user_id: str) -> User | None:
        return await User.find_one(User.id == ObjectId(user_id))
