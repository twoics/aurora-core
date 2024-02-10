from typing import List

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import Path
from starlette.responses import Response

from app.dependencies.auth import get_admin_user
from app.dependencies.auth import get_current_user
from app.dependencies.repo import matrix_repo
from app.dependencies.repo import user_repo
from app.dependencies.valid import matrix_uuid_exist
from app.dependencies.valid import user_in_group
from app.dependencies.valid import user_not_in_group
from app.dependencies.valid import username_is_exist
from app.dto.matrix import MatrixCreate
from app.dto.matrix import MatrixDetailGet
from app.dto.matrix import MatrixGet
from app.dto.matrix import MatrixUpdate
from app.models import User
from app.repo.matrix.proto import MatrixRepo
from app.repo.user.proto import UserRepo

router = APIRouter()


@router.post('/', dependencies=[Depends(get_admin_user)])
async def create_matrix(
    data: MatrixCreate = Body(),
    repo: MatrixRepo = Depends(matrix_repo),
):
    """Create a new matrix"""

    await repo.create(data)
    return Response(status_code=201)


@router.put(
    '/{uuid}',
    dependencies=[Depends(get_admin_user), Depends(matrix_uuid_exist)],
    response_model=MatrixDetailGet,
)
async def update_matrix(
    uuid: str = Path(),
    data: MatrixUpdate = Body(),
    repo: MatrixRepo = Depends(matrix_repo),
):
    """Update an existing matrix"""

    await repo.update_matrix(uuid, data)
    return await repo.get_by_uuid(data.uuid)


@router.post(
    '/{uuid}/add/{username}',
    dependencies=[
        Depends(get_admin_user),
        Depends(matrix_uuid_exist),
        Depends(username_is_exist),
        Depends(user_not_in_group),
    ],
)
async def add_matrix_user(
    uuid: str = Path(),
    username: str = Path(),
    m_repo: MatrixRepo = Depends(matrix_repo),
    u_repo: UserRepo = Depends(user_repo),
):
    """Add a user to the matrix users"""

    await m_repo.add_user(uuid, await u_repo.get_by_name(username))
    return Response(status_code=201)


@router.get('/my', response_model=List[MatrixGet])
async def my_matrices(
    user: User = Depends(get_current_user), repo: MatrixRepo = Depends(matrix_repo)
):
    """List all matrix what user have"""

    return await repo.user_matrices(user)


@router.get(
    '/{uuid}',
    dependencies=[Depends(get_admin_user), Depends(matrix_uuid_exist)],
    response_model=MatrixDetailGet,
)
async def get_matrix(
    uuid: str = Path(),
    repo: MatrixRepo = Depends(matrix_repo),
):
    """Get an existing matrix by uuid"""

    return await repo.detail_by_uuid(uuid)


@router.delete(
    '/{uuid}/remove/{username}',
    dependencies=[
        Depends(get_admin_user),
        Depends(matrix_uuid_exist),
        Depends(username_is_exist),
        Depends(user_in_group),
    ],
)
async def remove_matrix_user(
    uuid: str = Path(),
    username: str = Path(),
    m_repo: MatrixRepo = Depends(matrix_repo),
    u_repo: UserRepo = Depends(user_repo),
):
    """Remove a user from the matrix users"""

    await m_repo.remove_user(uuid, await u_repo.get_by_name(username))
    return Response(status_code=204)
