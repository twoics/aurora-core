from typing import List
from typing import Protocol

from dto.client import ClientCreate
from models import Client


class ClientRepo(Protocol):
    async def create(self, client: ClientCreate) -> str:
        """
        Create a new client and generate access key for this client
        :return:
        A raw access key for this client.
        Important!
        The hashed access key will be stored in the database, you cannot get it in its raw form again
        """

    async def exists(self, access_key: str) -> bool:
        """A raw access key value is expected. NOT hash"""

    async def get_all(self) -> List[Client]:
        """Get all stored clients"""
