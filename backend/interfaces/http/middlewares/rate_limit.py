import logging
from http import HTTPStatus

from redis.exceptions import RedisError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limiter, limits):
        super().__init__(app)
        self._limiter = limiter
        self._limits = limits

    async def dispatch(self, request: Request, call_next):
        route = request.scope.get('route')
        if not route:
            return await call_next(request)

        method = request.method
        path = route.path
        key_config = f'{method}:{path}'

        if key_config not in self._limits:
            return await call_next(request)

        limit, window = self._limits.get(key_config)
        ip = request.headers.get("x-forwarded-for", request.client.host)
        redis_key = f'rate:{key_config}:{ip}'

        try:
            is_allowed = self._limiter.is_allowed(
                key=redis_key,
                limit=limit,
                window=window,
            )
        except RedisError as e:
            logger.error('Rate limit error: %s', e)
            return await call_next(request)

        if not is_allowed:
            return JSONResponse(
                status_code=HTTPStatus.TOO_MANY_REQUESTS,
                content={
                    'detail': 'Too many requests',
                })
        return await call_next(request)
