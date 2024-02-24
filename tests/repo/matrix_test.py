import pytest
from beanie.exceptions import RevisionIdWasChanged
from dto.matrix import MatrixCreate
from dto.matrix import MatrixUpdate
from models import Matrix
from models import User
from repo.matrix.proto import MatrixRepo


class TestMatrixRepo:
    @pytest.mark.parametrize(
        'data',
        [
            MatrixCreate(uuid='0SN91roa6', name='Aurora'),
            MatrixCreate(uuid='CSNcFrZ68', name='Ambience'),
        ],
    )
    @pytest.mark.asyncio
    async def test_create(self, data, matrix_repo: MatrixRepo):
        await matrix_repo.create(data)
        assert await matrix_repo.get_by_uuid(data.uuid)

    @pytest.mark.parametrize(
        'data',
        [
            MatrixUpdate(uuid='CSNcFrZ68', name='Ambience', height=11),
            MatrixUpdate(uuid='HtBeGtX94', name='Char', height=22),
        ],
    )
    @pytest.mark.asyncio
    async def test_update(self, created_matrix: Matrix, matrix_repo: MatrixRepo, data):
        await matrix_repo.update(created_matrix.uuid, data)
        matrix = await matrix_repo.get_by_uuid(data.uuid)
        assert matrix.height == data.height and matrix.width == data.width
        assert matrix.name == data.name

    @pytest.mark.parametrize(
        'data',
        [
            MatrixUpdate(uuid='already-exists', name='Aurora'),
        ],
    )
    @pytest.mark.asyncio
    async def test_duplicate_update(
        self, created_matrix: Matrix, matrix_repo: MatrixRepo, data
    ):
        await matrix_repo.create(data)
        with pytest.raises(RevisionIdWasChanged):
            await matrix_repo.update(created_matrix.uuid, data)


class TestMatrixUser:
    @pytest.mark.asyncio
    async def test_add_user_to_matrix(
        self, created_matrix: Matrix, matrix_repo: MatrixRepo, created_user: User
    ):
        await matrix_repo.add_user(created_matrix.uuid, created_user)
        assert await matrix_repo.user_exists(created_matrix.uuid, created_user)

    @pytest.mark.asyncio
    async def test_remove_user(
        self, created_matrix: Matrix, matrix_repo: MatrixRepo, created_user: User
    ):
        await matrix_repo.add_user(created_matrix.uuid, created_user)
        await matrix_repo.remove_user(created_matrix.uuid, created_user)
        assert not await matrix_repo.user_matrices(created_user)

    @pytest.mark.asyncio
    async def test_user_doesnt_exist(
        self, created_matrix: Matrix, matrix_repo: MatrixRepo, created_user: User
    ):
        assert not await matrix_repo.user_exists(created_matrix.uuid, created_user)

    @pytest.mark.asyncio
    async def test_user_matrices_doesnt_exist(
        self, matrix_repo: MatrixRepo, created_user: User
    ):
        assert not await matrix_repo.user_matrices(created_user)

    @pytest.mark.asyncio
    async def test_get_user_matrices(
        self, created_matrix: Matrix, matrix_repo: MatrixRepo, created_user: User
    ):
        await matrix_repo.add_user(created_matrix.uuid, created_user)
        assert await matrix_repo.user_matrices(created_user)
