import logging

from fastapi import WebSocket
from fastapi import WebSocketException
from models import Client
from models import Matrix
from models import User
from repo.client.proto import ClientRepo
from repo.matrix.proto import MatrixRepo
from repo.user.proto import UserRepo
from services.auth.tokens import TokenAuth
from services.control.connection.session import Session
from starlette.status import WS_1003_UNSUPPORTED_DATA
from starlette.status import WS_1008_POLICY_VIOLATION

logger = logging.getLogger(__name__)


class ConnectionAgent:
    def __init__(
        self,
        matrix_uuid: str,
        websocket: WebSocket,
        matrix_repo: MatrixRepo,
        client_repo: ClientRepo,
        auth_service: TokenAuth,
        user_repo: UserRepo,
    ):
        self._ws = websocket
        self._matrix_repo = matrix_repo
        self._client_repo = client_repo
        self._auth_service = auth_service
        self._user_repo = user_repo
        self._uuid = matrix_uuid

    async def accept(self) -> Session:
        """Accept user connection through some client"""

        client = await self._get_client()

        logger.info('Client permissions have been verified. The client is valid')
        await self._ws.accept()
        logger.info('Websocket connection accepted')

        user = await self._get_user()
        logger.info(f'User {user.username} initiate connect to matrix {self._uuid}')
        matrix = await self._get_user_matrix(user)

        logger.info('User connected successfully. Great')
        return Session(user=user, matrix=matrix, client=client)

    async def _get_user_matrix(self, user: User) -> Matrix:
        """Validate user access to current matrix"""

        if (
            not (matrix := await self._matrix_repo.get_by_uuid(self._uuid))
            or not await self._matrix_repo.user_exists(self._uuid, user)
            or not user.is_matrices_access
        ):
            logger.info(
                f'User {user.username} does not have access to this matrix. Denied'
            )
            raise WebSocketException(WS_1003_UNSUPPORTED_DATA, 'Unsupported UUID')
        return matrix

    async def _get_client(self) -> Client:
        """Validate client access key for connect and return client for this key"""

        key = self._ws.query_params.get('access_key', '')
        if not (client := await self._client_repo.get_by_key(key)):
            logger.info(f'Someone tried to connect with wrong access key {key}')
            raise WebSocketException(WS_1003_UNSUPPORTED_DATA, 'Unsupported access key')
        return client

    async def _get_user(self) -> User:
        """Get user by token in query params"""

        token = self._ws.query_params.get('token')
        if not token:
            raise WebSocketException(
                WS_1008_POLICY_VIOLATION, reason='Token is required'
            )
        if not (claims := await self._auth_service.decode(token)):
            raise WebSocketException(WS_1008_POLICY_VIOLATION, reason='Access denied')
        return await self._user_repo.get_by_id(claims['sub'])
