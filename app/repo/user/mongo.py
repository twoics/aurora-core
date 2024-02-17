from beanie.odm.operators.update.general import Set
from bson import ObjectId
from dto.user import UserRegister
from dto.user import UserUpdate
from models import User
from repo.user.proto import UserRepo
from services.auth.credentials import get_password_hash


class UserMongoRepository(UserRepo):
    async def get_by_name(self, username: str) -> User | None:
        """Find user with this username and return it"""

        return await User.find_one(User.username == username)

    async def create_user(self, user: UserRegister) -> None:
        """Create user and hash his password"""

        data = user.model_dump()
        data['password'] = get_password_hash(data['password'])
        await User(**data).insert()

    async def update_user(self, username: str, user: UserUpdate) -> None:
        """Update user with given username and set UserUpdate data"""

        await User.find_one(User.username == username).update(Set((user.model_dump())))

    async def get_by_id(self, user_id: str) -> User | None:
        """Get user by user_id as str, it will be converted into ObjectID"""

        return await User.find_one(User.id == ObjectId(user_id))

    async def block_user(self, user: User) -> None:
        """Block the user so that he cannot connect to matrices"""

        user.is_block = True
        await user.save()
