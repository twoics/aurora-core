from dependencies.repo import get_user_repo
from fastapi import Depends
from fastapi import HTTPException
from models import User
from repo.user.proto import UserRepo
from starlette import status


async def get_user_by_username(
    username: str, repo: UserRepo = Depends(get_user_repo)
) -> User:
    """Get user by username variable in path"""

    if not (user := await repo.get_by_name(username)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user
