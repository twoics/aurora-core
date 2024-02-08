from app.dto.matrix import MatrixCreate
from app.models import Matrix
from app.repo.matrix.proto import MatrixRepo


class MatrixMongoRepository(MatrixRepo):
    async def create(self, matrix: MatrixCreate) -> None:
        await Matrix(**matrix.model_dump(), users=[]).insert()
