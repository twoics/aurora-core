from typing import TypedDict

from beanie.odm.operators.update.general import Set
from dto.client import ClientCreate
from models import Client
from repo.client.proto import ClientRepo
from utils.access import gen_access_key
from utils.access import get_key_hash


class AccessKey(TypedDict):
    access_key: str
    hashed_access_key: str


class MongoClientRepo(ClientRepo):
    async def create(self, client: ClientCreate) -> str:
        key = gen_access_key()
        await Client(**client.model_dump(), access_key=key['hashed_access_key'])
        return key['access_key']

    async def renew_access(self, client: Client):
        key = gen_access_key()
        await client.update(Set({Client.access_key: key['hashed_access_key']}))
        return key['access_key']

    async def exists(self, access_key: str) -> bool:
        hashed_access_key = get_key_hash(access_key)
        return bool(await Client.find_one(Client.access_key == hashed_access_key))
