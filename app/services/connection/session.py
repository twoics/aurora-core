from dataclasses import dataclass

from models import Client
from models import Matrix
from models import User


@dataclass(frozen=True)
class Session:
    user: User
    matrix: Matrix
    client: Client
