from fastapi import APIRouter
from fastapi import Body
from fastapi import HTTPException
from starlette import status
from starlette.responses import Response

from app.dto.user import UserRegister
from app.repo.user import UserRepository

router = APIRouter()


@router.post('/register')
async def register(user: UserRegister = Body(...)):
    """Register user by username and password"""

    exist_user = await UserRepository.get_by_name(user.username)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists'
        )
    await UserRepository.create_user(UserRegister(**user.dict()))
    return Response(status_code=status.HTTP_201_CREATED)
