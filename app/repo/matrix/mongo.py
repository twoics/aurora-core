from beanie.odm.operators.update.array import Pull
from beanie.odm.operators.update.array import Push
from beanie.odm.operators.update.general import Set

from app.dto.matrix import MatrixCreate
from app.dto.matrix import MatrixGet
from app.dto.matrix import MatrixUpdate
from app.models import Matrix
from app.models import User
from app.repo.matrix.proto import MatrixRepo


class MatrixMongoRepository(MatrixRepo):
    async def get_by_uuid(self, matrix_uuid: str) -> Matrix | None:
        return await Matrix.find_one(Matrix.uuid == matrix_uuid)

    async def detail_by_uuid(self, matrix_uuid: str) -> MatrixGet | None:
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
                projection_model=MatrixGet,
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
