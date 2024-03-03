from typing import List
from typing import TypedDict

from dto.client import ClientCreate
from models import Client
from repo.client.proto import ClientRepo
from utils.access import gen_access_key
from utils.access import get_key_hash


class AccessKey(TypedDict):
    access_key: str
    hashed_access_key: str


class ClientMongoRepository(ClientRepo):
    async def create(self, client: ClientCreate) -> str:
        key = gen_access_key()
        await Client(
            **client.model_dump(), access_key=key['hashed_access_key']
        ).insert()
        return key['access_key']

    async def get_by_key(self, access_key: str) -> Client | None:
        hashed_access_key = get_key_hash(access_key)
        return await Client.find_one(Client.access_key == hashed_access_key)

    async def exists(self, access_key: str) -> bool:
        return bool(await self.get_by_key(access_key))

    async def get_all(self) -> List[Client]:
        return await Client.all().to_list()
