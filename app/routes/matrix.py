from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from starlette.responses import Response

from app.dependencies.auth import get_admin_user
from app.dependencies.repo import matrix_repo
from app.dto.matrix import MatrixCreate
from app.repo.matrix.proto import MatrixRepo

router = APIRouter()


@router.post('/', dependencies=[Depends(get_admin_user)])
async def create_matrix(
    repo: MatrixRepo = Depends(matrix_repo), data: MatrixCreate = Body()
):
    """Create a new matrix"""
    await repo.create(data)
    return Response(status_code=201)
