from deps.config import get_settings
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify(hash_res: str, source: str) -> bool:
    """Verify the user current password hashed from this raw password"""

    return pwd_context.verify(source, hash_res)


def generate_hash(source: str) -> str:
    """Return the hash of password"""

    conf = get_settings()
    return pwd_context.hash(source, salt=conf.HASH_SALT)
