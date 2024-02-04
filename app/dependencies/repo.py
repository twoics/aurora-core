from app.repo.user.mongo import UserMongoRepository
from app.repo.user.proto import UserRepo


async def user_repo() -> UserRepo:
    """Get user repository"""

    return UserMongoRepository()
