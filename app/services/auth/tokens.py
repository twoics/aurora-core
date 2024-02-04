from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import TypedDict

from jose import jwt
from jose import JWTError

from app.config.config import Settings
from app.models import User


class Tokens(TypedDict):
    access_token: str
    refresh_token: str


class TokenAuth:
    def __init__(self, conf: Settings):
        self._conf = conf

    async def decode_token(self, token) -> dict | None:
        """Return claims of this token if token valid else None"""

        try:
            return jwt.decode(
                token, self._conf.SECRET_KEY, algorithms=[self._conf.ALGORITHM]
            )
        except JWTError:
            return None

    async def can_renew_tokens(self, access_token: str, refresh_token: str) -> bool:
        """Check access token and refresh are valid"""

        claims = await self.decode_token(refresh_token)
        return claims and claims.get('access_token') == access_token

    async def generate_tokens(self, user: User) -> Tokens:
        """Generate a pair of access tokens and refresh"""

        access_token = await self._generate_token(
            user, self._conf.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        refresh_token = await self._generate_token(
            user, self._conf.REFRESH_TOKEN_EXPIRE_MINUTES, access_token=access_token
        )
        return {'access_token': access_token, 'refresh_token': refresh_token}

    async def _generate_token(self, user: User, expire_minutes: int, **kwargs) -> str:
        """Generate a JWT token"""

        expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
        to_encode = {'exp': expire, 'sub': str(user.id), **kwargs}
        encoded_jwt = jwt.encode(
            to_encode, self._conf.SECRET_KEY, algorithm=self._conf.ALGORITHM
        )
        return encoded_jwt
