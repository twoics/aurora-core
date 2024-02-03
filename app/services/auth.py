from passlib.context import CryptContext

from app.models import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(user: User, password: str) -> bool:
    return pwd_context.verify(password, user.password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
