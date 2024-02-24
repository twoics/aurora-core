import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging incoming requests and response statuses for them"""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        logger = logging.getLogger(__name__)
        logger.info(f'{request.method} {request.url}')
        response = await call_next(request)
        logger.info(f'Response status {response.status_code}')
        return response
