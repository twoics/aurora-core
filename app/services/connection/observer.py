import dataclasses
import logging

from config.config import Settings
from fastapi import WebSocketException
from fastapi_limiter.depends import WebSocketRateLimiter
from services.connection.session import Session
from services.pool.proto import MatrixConnectionsPool
from starlette.status import WS_1008_POLICY_VIOLATION
from starlette.websockets import WebSocket
from starlette.websockets import WebSocketDisconnect

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class Context:
    websocket: WebSocket
    session: Session
    pool: MatrixConnectionsPool
    config: Settings


class Inspector:
    def __init__(self, context: Context, ratelimit: WebSocketRateLimiter):
        self._ratelimit = ratelimit
        self._ws = context.websocket
        self._pool = context.pool
        self._session = context.session

    async def _get_rate_key(self) -> str:
        """Get a key for the ratelimit"""

        sess_dict = dataclasses.asdict(self._session)
        user, matrix, client = (
            sess_dict['user'],
            sess_dict['matrix'],
            sess_dict['client'],
        )
        return f'{user.id}:{client.id}:{matrix.uuid}'

    async def inspect_user(self) -> None:
        """Check user permissions and raise ws exception if something wrong"""

        user, matrix = self._session.user, self._session.matrix
        await self._ratelimit(self._ws, self._get_rate_key())
        if not await self._pool.is_connected(user, matrix):
            raise WebSocketException(WS_1008_POLICY_VIOLATION, 'Access denied')


class ConnectionObserver:
    def __init__(self, context: Context):
        self._ws = context.websocket
        self._pool = context.pool
        self._context = context
        self._matrix, self._user, self._config = (
            context.session.matrix,
            context.session.user,
            context.config,
        )

    async def __aenter__(self) -> Inspector:
        """Add user in connection pool"""

        limit = WebSocketRateLimiter(
            seconds=1, times=self._config.WS_QUERY_COUNT_PER_SECOND
        )
        await self._pool.connect(self._user, self._matrix)
        logger.info(f'Put {self._user.username}:{self._matrix.uuid} connection to pool')

        return Inspector(ratelimit=limit, context=self._context)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Remove user from connection pool"""

        await self._pool.disconnect(self._user, self._matrix)
        logger.info(f'Delete {self._user.username}:{self._matrix.uuid} from pool')
        logger.info('Connection in pool closed')

        if exc_type is WebSocketDisconnect:
            return True


class ObserverFactory:
    def __init__(
        self, websocket: WebSocket, pool: MatrixConnectionsPool, config: Settings
    ):
        self._ws = websocket
        self._pool = pool
        self._config = config

    def get_observer(self, session: Session) -> ConnectionObserver:
        """Create observer for inspect this session"""

        context = Context(
            websocket=self._ws, session=session, pool=self._pool, config=self._config
        )
        return ConnectionObserver(context=context)
