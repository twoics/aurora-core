import uuid
from typing import TypedDict

from utils.hashing import generate_hash


class AccessKey(TypedDict):
    access_key: str
    hashed_access_key: str


def gen_access_key() -> AccessKey:
    """Generate an access key"""

    access_key = uuid.uuid4().hex
    return {'access_key': access_key, 'hashed_access_key': get_key_hash(access_key)}


def get_key_hash(access_key: str) -> str:
    """Generate a hash of an access key"""

    return generate_hash(access_key)
