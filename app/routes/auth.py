from dependencies.auth import get_auth_service
from dependencies.auth import get_current_user
from dependencies.repo import user_repo
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm as OAuthForm
from models import User
from repo.user.proto import UserRepo
from services.auth.credentials import verify_password
from services.auth.tokens import TokenAuth
from starlette import status

router = APIRouter()


@router.post('/login')
async def login(
    form_data: OAuthForm = Depends(OAuthForm),
    auth_service: TokenAuth = Depends(get_auth_service),
    repo: UserRepo = Depends(user_repo),
):
    """Login user by username and password"""

    exist_user = await repo.get_by_name(form_data.username)
    if not exist_user or not verify_password(exist_user, form_data.password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Wrong credentials')

    return {**await auth_service.generate_tokens(exist_user)}


@router.post('/refresh')
async def refresh(
    refresh_token: str,
    access_token: str,
    user: User = Depends(get_current_user),
    auth_service: TokenAuth = Depends(get_auth_service),
):
    """Refresh token pair by refresh token"""

    if not await auth_service.can_renew_tokens(access_token, refresh_token):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Token has expired')
    return {**await auth_service.generate_tokens(user)}
