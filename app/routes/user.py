from dependencies.auth import get_admin_user
from dependencies.repo import user_repo
from dto.user import UserRegister
from dto.user import UserUpdate
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path
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
