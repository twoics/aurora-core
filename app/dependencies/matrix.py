from dependencies.repo import get_matrix_repo
from fastapi import Depends
from fastapi import HTTPException
from models import Matrix
from repo.matrix.proto import MatrixRepo
from starlette import status


async def get_matrix_by_uuid(
    uuid: str, repo: MatrixRepo = Depends(get_matrix_repo)
) -> Matrix:
    """Get user by username variable in path"""

    if not (matrix := await repo.get_by_uuid(uuid)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return matrix
