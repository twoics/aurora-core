from config.config import Settings
from dependencies.config import get_settings
from dependencies.repo import get_user_repo
from fastapi import Depends
from fastapi import HTTPException
from fastapi import WebSocket
from fastapi import WebSocketException
from fastapi.security import OAuth2PasswordBearer
from models import User
from repo.user.proto import UserRepo
from services.auth.tokens import TokenAuth
from starlette import status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


def get_auth_service(conf: Settings = Depends(get_settings)) -> TokenAuth:
    """Get auth service customized by application configuration"""

    return TokenAuth(conf)


async def get_current_user(
    access_token: str = Depends(oauth2_scheme),
    auth_service: TokenAuth = Depends(get_auth_service),
    repo: UserRepo = Depends(get_user_repo),
) -> User:
    """Validate access token and return user by this token"""

    if not (claims := await auth_service.decode_token(access_token)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Access denied')
    return await repo.get_by_id(claims['sub'])


async def get_admin_user(user: User = Depends(get_current_user)) -> User:
    """Validate access token and return user by this token if user is admin"""

    if not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='You have no rights')
    return user


async def get_user_by_ws(
    request: WebSocket,
    auth_service: TokenAuth = Depends(get_auth_service),
    repo: UserRepo = Depends(get_user_repo),
):
    """Get user from token in websocket query params"""

    token = request.query_params.get('token')
    if not token:
        raise WebSocketException(
            status.WS_1008_POLICY_VIOLATION, reason='Token is required'
        )
    if not (claims := await auth_service.decode_token(token)):
        raise WebSocketException(
            status.WS_1008_POLICY_VIOLATION, reason='Access denied'
        )
    return await repo.get_by_id(claims['sub'])
