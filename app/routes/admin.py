from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from starlette import status
from starlette.responses import Response

from app.dependencies.auth import get_admin_user
from app.dependencies.repo import user_repo
from app.dto.user import UserRegister
from app.repo.user.proto import UserRepo

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
    return Response(status.HTTP_201_CREATED)
