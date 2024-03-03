import logging
from functools import wraps
from typing import List

from deps.auth import get_admin_user
from deps.auth import get_current_user
from deps.group import matrix_uuid_exist
from deps.group import user_in_group
from deps.group import user_not_in_group
from deps.matrix import get_matrix_by_uuid
from deps.pool import get_matrix_connections_pool
from deps.repo import get_matrix_repo
from deps.user import get_user_by_username
from dto.matrix import MatrixCreate
from dto.matrix import MatrixDetailGet
from dto.matrix import MatrixGet
from dto.matrix import MatrixUpdate
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
from models import Matrix
from models import User
from repo.matrix.proto import MatrixRepo
from services.pool.proto import MatrixConnectionsPool
from starlette import status
from starlette.responses import Response

router = APIRouter()
logger = logging.getLogger(__name__)


def matrix_not_exists(endpoint):
    """Decorator for check that matrix with given uuid for create/update already exists"""

    @wraps(endpoint)
    async def wrapped_endpoint(**kwargs):
        matrix_repo, uuid = kwargs['matrix_repo'], kwargs['data'].uuid
        matrix_exists = await matrix_repo.get_by_uuid(uuid)
        if matrix_exists:
            logger.info(f'Matrix with {uuid} uuid already exists')
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, detail='Matrix already exists'
            )
        return await endpoint(**kwargs)

    return wrapped_endpoint


@router.post('/', dependencies=[Depends(get_admin_user)])
@matrix_not_exists
async def create_matrix(
    data: MatrixCreate = Body(),
    matrix_repo: MatrixRepo = Depends(get_matrix_repo),
):
    """Create a new matrix"""

    await matrix_repo.create(data)
    return Response(status_code=status.HTTP_201_CREATED)


@router.put(
    '/{uuid}',
    dependencies=[Depends(get_admin_user), Depends(matrix_uuid_exist)],
    response_model=MatrixDetailGet,
)
@matrix_not_exists
async def update_matrix(
    uuid: str = Path(),
    data: MatrixUpdate = Body(),
    matrix_repo: MatrixRepo = Depends(get_matrix_repo),
):
    """Update an existing matrix"""

    await matrix_repo.update(uuid, data)
    return await matrix_repo.get_by_uuid(data.uuid)


@router.post(
    '/{uuid}/add/{username}',
    dependencies=[
        Depends(get_admin_user),
        Depends(matrix_uuid_exist),
        Depends(user_not_in_group),
    ],
)
async def add_matrix_user(
    uuid: str = Path(),
    user: User = Depends(get_user_by_username),
    matrix_repo: MatrixRepo = Depends(get_matrix_repo),
):
    """Add a user to the matrix users"""

    await matrix_repo.add_user(uuid, user)
    return Response(status_code=status.HTTP_201_CREATED)


@router.get('/my', response_model=List[MatrixGet])
async def my_matrices(
    user: User = Depends(get_current_user),
    matrix_repo: MatrixRepo = Depends(get_matrix_repo),
):
    """List all matrix what user have"""

    return await matrix_repo.user_matrices(user)


@router.get(
    '/{uuid}',
    dependencies=[Depends(get_admin_user), Depends(matrix_uuid_exist)],
    response_model=MatrixDetailGet,
)
async def get_matrix(
    uuid: str = Path(),
    matrix_repo: MatrixRepo = Depends(get_matrix_repo),
):
    """Get an existing matrix by uuid"""

    return await matrix_repo.detail_by_uuid(uuid)


@router.delete(
    '/{uuid}/remove/{username}',
    dependencies=[
        Depends(get_admin_user),
        Depends(matrix_uuid_exist),
        Depends(user_in_group),
    ],
)
async def remove_matrix_user(
    uuid: str = Path(),
    user: User = Depends(get_user_by_username),
    matrix_repo: MatrixRepo = Depends(get_matrix_repo),
):
    """Remove a user from the matrix users"""

    await matrix_repo.remove_user(uuid, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/{uuid}/{username}/disconnect', dependencies=[Depends(get_admin_user)])
async def disconnect_user(
    user: User = Depends(get_user_by_username),
    matrix: Matrix = Depends(get_matrix_by_uuid),
    pool: MatrixConnectionsPool = Depends(get_matrix_connections_pool),
):
    """Disconnect user from all connections"""

    await pool.disconnect_all(user, matrix)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
