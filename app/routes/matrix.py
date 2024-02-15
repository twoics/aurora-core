from typing import List

from dependencies.auth import get_admin_user
from dependencies.auth import get_current_user
from dependencies.group import matrix_uuid_exist
from dependencies.group import user_in_group
from dependencies.group import user_not_in_group
from dependencies.group import username_is_exist
from dependencies.repo import matrix_repo
from dependencies.repo import user_repo
from dto.matrix import MatrixCreate
from dto.matrix import MatrixDetailGet
from dto.matrix import MatrixGet
from dto.matrix import MatrixUpdate
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import Path
from models import User
from repo.matrix.proto import MatrixRepo
from repo.user.proto import UserRepo
from starlette.responses import Response

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
