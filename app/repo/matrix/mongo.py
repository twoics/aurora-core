import typing

from beanie.odm.operators.find.comparison import In
from beanie.odm.operators.update.array import Pull
from beanie.odm.operators.update.array import Push
from beanie.odm.operators.update.general import Set
from dto.matrix import MatrixCreate
from dto.matrix import MatrixDetailGet
from dto.matrix import MatrixUpdate
from models import Matrix
from models import User
from repo.matrix.proto import MatrixRepo


class MatrixMongoRepository(MatrixRepo):
    async def get_by_uuid(self, matrix_uuid: str) -> Matrix | None:
        return await Matrix.find_one(Matrix.uuid == matrix_uuid)

    async def get_many(self, matrix_uuids: typing.List[str]) -> typing.List[Matrix]:
        return await Matrix.find(In(Matrix.uuid, matrix_uuids)).to_list()

    async def detail_by_uuid(self, matrix_uuid: str) -> MatrixDetailGet | None:
        return (
            await (await self.get_by_uuid(matrix_uuid))
            .aggregate(
                [
                    {
                        '$lookup': {
                            'from': 'user',
                            'localField': 'users',
                            'foreignField': '_id',
                            'as': 'users',
                        }
                    }
                ],
                projection_model=MatrixDetailGet,
            )
            .to_list()
        )[0]

    async def create(self, matrix: MatrixCreate) -> None:
        await Matrix(**matrix.model_dump(), users=[]).insert()

    async def update_matrix(self, matrix_uuid: str, matrix: MatrixUpdate) -> None:
        await (await self.get_by_uuid(matrix_uuid)).update(Set(matrix.model_dump()))

    async def add_user(self, matrix_uuid: str, user: User) -> None:
        await (await self.get_by_uuid(matrix_uuid)).update(
            Push({Matrix.users: user.id})
        )

    async def remove_user(self, matrix_uuid: str, user: User) -> None:
        await (await self.get_by_uuid(matrix_uuid)).update(
            Pull({Matrix.users: user.id})
        )

    async def user_exists(self, matrix_uuid: str, user: User) -> bool:
        return bool(await Matrix.find_one(Matrix.users == user.id))

    async def user_matrices(self, user: User) -> typing.List[Matrix]:
        return await Matrix.find_many(Matrix.users == user.id).to_list()
