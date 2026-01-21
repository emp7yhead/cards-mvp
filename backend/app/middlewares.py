from fastapi import FastAPI

from backend.app.container import container
from backend.infrastructure.rate_limit.redis_rate_limiter import (
    RATE_LIMITS,
)
from backend.interfaces.http.middlewares.rate_limit import RateLimitMiddleware
from backend.interfaces.http.middlewares.request_id import RequestIdMiddleware


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(
        RateLimitMiddleware,
        limiter=container.redis_rate_limiter,
        limits=RATE_LIMITS,
    )
