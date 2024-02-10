from fastapi import Depends

from app.dependencies.repo import matrix_repo
from app.dependencies.repo import user_repo
from app.repo.matrix.proto import MatrixRepo
from app.repo.user.proto import UserRepo


async def user_in_matrix_group(
    uuid: str,
    username: str,
    m_repo: MatrixRepo = Depends(matrix_repo),
    u_repo: UserRepo = Depends(user_repo),
) -> bool:
    """Checks if a user in a matrix group"""

    return await m_repo.user_exists(uuid, await u_repo.get_by_name(username))
