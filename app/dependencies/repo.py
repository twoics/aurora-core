from app.repo.user import UserRepository


async def user_repo() -> UserRepository:
    """Get user repository"""

    return UserRepository()
