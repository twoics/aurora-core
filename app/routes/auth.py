from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import HTTPException
from starlette import status
from starlette.responses import Response

from app.dependencies import get_auth_service
from app.dto.user import UserLogin
from app.dto.user import UserRegister
from app.repo.user import UserRepository
from app.services.auth.credentials import verify_password
from app.services.auth.tokens import TokenAuth

router = APIRouter()


@router.post('/register')
async def register(user: UserRegister = Body(...)):
    """Register user by username and password"""

    exist_user = await UserRepository.get_by_name(user.username)
    if exist_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='User already exists')

    await UserRepository.create_user(UserRegister(**user.dict()))
    return Response(status.HTTP_201_CREATED)


@router.post('/login')
async def login(
    login_user: UserLogin = Body(...),
    auth_service: TokenAuth = Depends(get_auth_service),
):
    """Login user by username and password"""

    exist_user = await UserRepository.get_by_name(login_user.username)
    if not exist_user or not verify_password(exist_user, login_user.password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Wrong credentials')

    return {**await auth_service.generate_tokens(exist_user)}
