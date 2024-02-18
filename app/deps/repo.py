from repo.matrix.mongo import MatrixMongoRepository
from repo.matrix.proto import MatrixRepo
from repo.user.mongo import UserMongoRepository
from repo.user.proto import UserRepo


async def get_user_repo() -> UserRepo:
    """Get user repository"""

    return UserMongoRepository()


async def get_matrix_repo() -> MatrixRepo:
    """Get matrix repository"""

    return MatrixMongoRepository()
