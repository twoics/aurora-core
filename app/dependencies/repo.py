from app.repo.matrix.mongo import MatrixMongoRepository
from app.repo.matrix.proto import MatrixRepo
from app.repo.user.mongo import UserMongoRepository
from app.repo.user.proto import UserRepo


async def user_repo() -> UserRepo:
    """Get user repository"""

    return UserMongoRepository()


async def matrix_repo() -> MatrixRepo:
    """Get matrix repository"""

    return MatrixMongoRepository()
