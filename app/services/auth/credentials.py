from passlib.context import CryptContext

from app.models import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(user: User, raw_password: str) -> bool:
    """Verify the user current password hashed from this raw password"""

    return pwd_context.verify(raw_password, user.password)


def get_password_hash(password: str) -> str:
    """Return the hash of password"""

    return pwd_context.hash(password)
