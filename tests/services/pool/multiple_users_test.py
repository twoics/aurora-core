from typing import List

import pytest
from models import Matrix
from models import User
from services.pool.proto import MatrixConnectionsPool


class TestMultipleUserConnection:
    @pytest.mark.asyncio
    async def test_multiple_users_connected(
        self,
        connection_pool: MatrixConnectionsPool,
        users: List[User],
        matrices: List[Matrix],
    ):
        await connection_pool.connect(users[0], matrices[0])
        await connection_pool.connect(users[1], matrices[1])

        assert await connection_pool.is_connected(users[0])
        assert await connection_pool.is_connected(users[1])

    @pytest.mark.asyncio
    async def test_connect_to_same_matrix(
        self,
        connection_pool: MatrixConnectionsPool,
        users: List[User],
        matrices: List[Matrix],
    ):
        await connection_pool.connect(users[0], matrices[0])
        await connection_pool.connect(users[1], matrices[0])

        assert await connection_pool.is_connected(users[0])
        assert await connection_pool.is_connected(users[1])

    @pytest.mark.asyncio
    async def test_disconnect_not_impact_to_another(
        self,
        connection_pool: MatrixConnectionsPool,
        users: List[User],
        matrices: List[Matrix],
    ):
        await connection_pool.connect(users[0], matrices[0])
        await connection_pool.connect(users[1], matrices[0])

        await connection_pool.disconnect(users[0])

        assert not await connection_pool.is_connected(users[0])
        assert await connection_pool.is_connected(users[1])
