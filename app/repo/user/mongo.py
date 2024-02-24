import uuid

from beanie.odm.operators.update.general import Set
from bson import ObjectId
from dto.user import UserRegister
from dto.user import UserUpdate
from models import User
from repo.user.proto import UserRepo
from utils.hashing import generate_hash


class UserMongoRepository(UserRepo):
    async def get_by_name(self, username: str) -> User | None:
        return await User.find_one(User.username == username)

    async def renew_access_key(self, user: User) -> str:
        access_key = uuid.uuid4().hex
        await user.update(Set({User.access_key: generate_hash(access_key)}))
        return access_key

    async def create_user(self, user: UserRegister) -> None:
        data = user.model_dump()
        data['password'] = generate_hash(data['password'])
        await User(**data).insert()

    async def update_user(self, username: str, user: UserUpdate) -> None:
        await User.find_one(User.username == username).update(Set((user.model_dump())))

    async def get_by_id(self, user_id: str) -> User | None:
        return await User.find_one(User.id == ObjectId(user_id))

    async def block_user(self, user: User) -> None:
        await self._update_matrix_access(user, matrix_access=False)

    async def unblock_user(self, user: User) -> None:
        await self._update_matrix_access(user, matrix_access=True)

    async def get_by_access_key(self, access_key: str) -> User | None:
        hashed_key = generate_hash(access_key)
        return await User.find_one(User.access_key == hashed_key)

    @staticmethod
    async def _update_matrix_access(user: User, matrix_access: bool) -> None:
        user.is_matrices_access = matrix_access
        await user.save()
