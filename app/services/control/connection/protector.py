import logging

from fastapi import WebSocket
from fastapi import WebSocketException
from models import User
from repo.client.proto import ClientRepo
from repo.matrix.proto import MatrixRepo
from starlette.status import WS_1003_UNSUPPORTED_DATA

logger = logging.getLogger(__name__)


class ConnectionProtector:
    def __init__(
        self, websocket: WebSocket, matrix_repo: MatrixRepo, client_repo: ClientRepo
    ):
        self._ws = websocket
        self._matrix_repo = matrix_repo
        self._client_repo = client_repo

    async def perms_valid(self, user: User, uuid: str):
        """Validate user access to current matrix"""

        if (
            not await self._matrix_repo.get_by_uuid(uuid)
            or not await self._matrix_repo.user_exists(uuid, user)
            or not user.is_matrices_access
        ):
            logger.info(f'User {user.username} does not have access to this matrix')
            raise WebSocketException(WS_1003_UNSUPPORTED_DATA, 'Unsupported UUID')

    async def client_valid(self):
        """Validate client access key for connect"""

        key = self._ws.query_params.get('access_key', '')
        if not (await self._client_repo.exists(key)):
            logger.info(f'Someone tried to connect with wrong access key {key}')
            raise WebSocketException(WS_1003_UNSUPPORTED_DATA, 'Unsupported access key')
