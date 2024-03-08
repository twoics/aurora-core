from typing import List

import pytest
from models import Matrix
from models import User
from services.pool.proto import MatrixConnectionsPool


class TestMultipleMatricesConnection:
    @pytest.mark.asyncio
    async def test_unable_connect_to_another_matrix_while_current_connection_active(
        self,
        connection_pool: MatrixConnectionsPool,
        created_user: User,
        matrices: List[Matrix],
    ):
        await connection_pool.connect(created_user, matrices[0])

        with pytest.raises(ConnectionError):
            await connection_pool.connect(created_user, matrices[1])

    @pytest.mark.asyncio
    async def test_unable_connect_to_current_matrix_while_current_connection_active(
        self,
        connection_pool: MatrixConnectionsPool,
        created_user: User,
        matrices: List[Matrix],
    ):
        await connection_pool.connect(created_user, matrices[0])

        with pytest.raises(ConnectionError):
            await connection_pool.connect(created_user, matrices[0])

    @pytest.mark.asyncio
    async def test_able_connect_to_another_after_disconnect(
        self,
        connection_pool: MatrixConnectionsPool,
        created_user: User,
        matrices: List[Matrix],
    ):
        await connection_pool.connect(created_user, matrices[0])
        await connection_pool.disconnect(created_user)

        await connection_pool.connect(created_user, matrices[1])
        assert await connection_pool.is_connected(created_user)
