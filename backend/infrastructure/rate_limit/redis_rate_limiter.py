from backend.infrastructure.redis.client import get_client

RATE_LIMITS = {
    'POST:/sessions': (5, 60),
    'POST:/sessions/{id}/join': (10, 60),
    'POST:/sessions/{id}/answers': (3, 300),
    'GET:/topics': (60,60),
}

class RedisRateLimiter:
    def __init__(self):
        self._redis = get_client()

    def is_allowed(
        self,
        key: str,
        limit: int,
        window: int,
    ) -> bool:
        pipe = self._redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, window)
        count, _ = pipe.execute()
        return count <= limit
