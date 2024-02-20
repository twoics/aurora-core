import pytest
from models import User


class TestAuth:
    @pytest.mark.asyncio
    async def test_login(self, async_client, created_user: User, user_repo):
        response = await async_client.post(
            '/auth/login',
            data={'username': created_user.username, 'password': 'qwerty'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )

        assert response.status_code == 200
        assert response.json().get('access_token')
        assert response.json().get('refresh_token')
