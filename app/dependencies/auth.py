from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from app.config.config import Settings
from app.dependencies.config import get_settings
from app.models import User
from app.repo.user import UserRepository
from app.services.auth.tokens import TokenAuth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


def get_auth_service(conf: Settings = Depends(get_settings)) -> TokenAuth:
    """Get auth service customized by application configuration"""

    return TokenAuth(conf)


async def get_current_user(
    access_token: OAuth2PasswordBearer = Depends(oauth2_scheme),
    auth_service: TokenAuth = Depends(get_auth_service),
) -> User:
    """Validate access token and return user by this token"""

    if not (claims := await auth_service.decode_token(access_token)):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Access denied')
    return await UserRepository.get_by_id(claims['sub'])


async def get_admin_user(user: User = Depends(get_current_user)) -> User:
    """Validate access token and return user by this token if user is admin"""

    if not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Access denied')
    return user
