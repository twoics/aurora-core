import logging

from config.config import Settings
from fastapi import WebSocketException
from fastapi_limiter.depends import WebSocketRateLimiter
from services.connection.session import Session
from services.pool.proto import MatrixConnectionsPool
from starlette.status import WS_1008_POLICY_VIOLATION
from starlette.websockets import WebSocket

logger = logging.getLogger(__name__)


class ConnectionObserver:
    def __init__(
        self,
        session: Session,
        config: Settings,
        websocket: WebSocket,
        pool: MatrixConnectionsPool,
    ):
        # Set during call aenter
        self._ratelimit = None

        self._ws = websocket
        self._pool = pool
        self._matrix = session.matrix
        self._user = session.user
        self._config = config
        self._client = session.client

    async def inspect(self) -> None:
        """Check client permissions and raise ws exception if something wrong"""

        if not self._ratelimit:
            raise ValueError('The method can be called after using with')

        await self._ratelimit(
            self._ws,
            context_key=f'{self._user.id}:{self._client.id}:{self._matrix.uuid}',
        )
        if not await self._pool.is_connected(self._user, self._matrix):
            raise WebSocketException(WS_1008_POLICY_VIOLATION, 'Access denied')

    async def __aenter__(self):
        """Add user in connection pool"""

        self._ratelimit = WebSocketRateLimiter(
            seconds=1, times=self._config.WS_QUERY_COUNT_PER_SECOND
        )
        await self._pool.connect(self._user, self._matrix)
        logger.info(f'Put {self._user.username}:{self._matrix.uuid} connection to pool')

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Remove user from connection pool"""

        await self._pool.disconnect(self._user, self._matrix)
        logger.info(f'Delete {self._user.username}:{self._matrix.uuid} from pool')
        logger.info('Connection in pool closed')
