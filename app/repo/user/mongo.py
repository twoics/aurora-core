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

    async def create(self, user: UserRegister) -> None:
        data = user.model_dump()
        data['password'] = generate_hash(data['password'])
        await User(**data).insert()

    async def update(self, username: str, user: UserUpdate) -> None:
        await User.find_one(User.username == username).update(Set((user.model_dump())))

    async def get_by_id(self, user_id: str) -> User | None:
        return await User.find_one(User.id == ObjectId(user_id))

    async def block(self, user: User) -> None:
        await self._update_matrix_access(user, matrix_access=False)

    async def unblock(self, user: User) -> None:
        await self._update_matrix_access(user, matrix_access=True)

    @staticmethod
    async def _update_matrix_access(user: User, matrix_access: bool) -> None:
        user.is_matrices_access = matrix_access
        await user.save()
