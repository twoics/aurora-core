from dependencies.repo import get_matrix_repo
from dependencies.repo import get_user_repo
from fastapi import Depends
from fastapi import HTTPException
from repo.matrix.proto import MatrixRepo
from repo.user.proto import UserRepo
from starlette import status


async def _user_in_matrix_group(
    uuid: str,
    username: str,
    m_repo: MatrixRepo = Depends(get_matrix_repo),
    u_repo: UserRepo = Depends(get_user_repo),
) -> bool:
    """Checks if a user in a matrix group"""

    return await m_repo.user_exists(uuid, await u_repo.get_by_name(username))


async def matrix_uuid_exist(uuid: str, repo: MatrixRepo = Depends(get_matrix_repo)):
    """Validate that matrix uuid exist"""

    if not await repo.get_by_uuid(uuid):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


async def user_in_group(exists: bool = Depends(_user_in_matrix_group)):
    """Validate if user in matrix group"""

    if not exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='User not in group'
        )


async def user_not_in_group(exists: bool = Depends(_user_in_matrix_group)):
    """Validate if user not in matrix group"""

    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='User already in group'
        )
