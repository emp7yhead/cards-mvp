from fastapi import FastAPI

from backend.app.container import container
from backend.infrastructure.rate_limit.redis_rate_limiter import (
    RATE_LIMITS,
)
from backend.interfaces.middlewares.rate_limit import RateLimitMiddleware


def setup_middlewares(app: FastAPI) -> None:
    print('setup')
    app.add_middleware(
        RateLimitMiddleware,
        limiter=container.redis_rate_limiter,
        limits=RATE_LIMITS,
    )
