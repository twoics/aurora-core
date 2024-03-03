import pytest
from models import User
from repo.user.proto import UserRepo


class TestAuth:
    @pytest.mark.asyncio
    async def test_login(self, async_client, created_user: User, user_repo: UserRepo):
        response = await async_client.post(
            '/auth/login',
            data={'username': created_user.username, 'password': 'qwerty'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )

        assert response.status_code == 200
        assert 'access_token' in response.json() and 'refresh_token' in response.json()
