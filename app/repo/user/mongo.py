from bson import ObjectId

from app.dto.user import UserRegister
from app.models import User
from app.repo.user.proto import UserRepo
from app.services.auth.credentials import get_password_hash


class UserMongoRepository(UserRepo):
    async def get_by_name(self, username: str) -> User | None:
        return await User.find_one(User.username == username)

    async def create_user(self, user: UserRegister) -> None:
        data = user.model_dump()
        data['password'] = get_password_hash(data['password'])
        await User(**data).insert()

    async def get_by_id(self, user_id: str) -> User | None:
        return await User.find_one(User.id == ObjectId(user_id))
