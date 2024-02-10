from fastapi import Depends
from fastapi import HTTPException
from starlette import status

from app.dependencies.repo import matrix_repo
from app.dependencies.repo import user_repo
from app.repo.matrix.proto import MatrixRepo
from app.repo.user.proto import UserRepo


async def matrix_uuid_exist(uuid: str, repo: MatrixRepo = Depends(matrix_repo)):
    """Validate that matrix uuid exist"""

    if not await repo.get_by_uuid(uuid):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


async def username_is_exist(username: str, repo: UserRepo = Depends(user_repo)):
    """Validate that user with username exist"""

    if not await repo.get_by_name(username):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
