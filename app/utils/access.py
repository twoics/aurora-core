import uuid
from typing import TypedDict

from utils.hashing import generate_hash


class AccessKey(TypedDict):
    access_key: str
    hashed_access_key: str


def _gen_access_key() -> AccessKey:
    """Generate an access key"""

    access_key = uuid.uuid4().hex
    return {'access_key': access_key, 'hashed_access_key': generate_hash(access_key)}
