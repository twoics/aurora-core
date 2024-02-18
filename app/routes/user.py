from dependencies.auth import get_admin_user
from dependencies.repo import user_repo
from dependencies.user import get_user_by_username
from dto.user import UserRegister
from dto.user import UserUpdate
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
from models import User
from repo.user.proto import UserRepo
from starlette import status
from starlette.responses import Response

router = APIRouter()


@router.post('/register', dependencies=[Depends(get_admin_user)])
async def register(
    user: UserRegister = Body(...),
    repo: UserRepo = Depends(user_repo),
):
    """Register user by username and password"""

    exist_user = await repo.get_by_name(user.username)
    if exist_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='User already exists')

    await repo.create_user(UserRegister(**user.dict()))
    return Response(status_code=status.HTTP_201_CREATED)


@router.put(
    '/{username}', dependencies=[Depends(get_admin_user)], response_model=UserUpdate
)
async def edit(
    username: str = Path(),
    user: UserUpdate = Body(),
    repo: UserRepo = Depends(user_repo),
):
    """Edit user info"""
    await repo.update_user(username, user)
    return await repo.get_by_name(user.username)


@router.post('/{username}/block', dependencies=[Depends(get_admin_user)])
async def block_user(
    user: User = Depends(get_user_by_username), repo: UserRepo = Depends(user_repo)
):
    """Block user access to start connection with all matrices. Even if it is in the matrix group"""

    await repo.block_user(user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/{username}/unblock', dependencies=[Depends(get_admin_user)])
async def unblock_user(
    user: User = Depends(get_user_by_username), repo: UserRepo = Depends(user_repo)
):
    """Return the ability to the user to create a connection with matrices"""

    await repo.unblock_user(user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
