import logging
from typing import List

from deps.auth import get_admin_user
from deps.repo import get_client_repo
from dto.client import ClientAccessKeyGet
from dto.client import ClientCreate
from dto.client import ClientGet
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from repo.client.proto import ClientRepo
from starlette import status

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/', dependencies=[Depends(get_admin_user)], response_model=List[ClientGet])
async def get_all_clients(repo: ClientRepo = Depends(get_client_repo)):
    """Get all created clients"""

    return await repo.get_all()


@router.post(
    '/',
    dependencies=[Depends(get_admin_user)],
    response_model=ClientAccessKeyGet,
    status_code=status.HTTP_201_CREATED,
)
async def create_access_key(
    client: ClientCreate = Body(...),
    repo: ClientRepo = Depends(get_client_repo),
):
    """Create a new client and return access token for this client"""

    return ClientAccessKeyGet(access_key=await repo.create(client))
