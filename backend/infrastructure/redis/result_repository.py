import orjson

from backend.domain.result.entities import Result
from backend.domain.session.value_objects import SessionId
from backend.infrastructure.redis.client import get_client
from backend.infrastructure.redis.serializers import (
    result_from_dict,
    result_to_dict,
)


class RedisResultRepository:

    def __init__(self):
        self._redis = get_client()

    def _key(self, session_id: SessionId) -> str:
        return f"result:{session_id}"

    def save(self, result: Result) -> None:
        key = self._key(result.session_id)
        self._redis.set(
            key,
            orjson.dumps(result_to_dict(result)),
        )

    def get(self, session_id: SessionId) -> Result | None:
        raw = self._redis.get(self._key(session_id))
        if not raw:
            return None
        return result_from_dict(orjson.loads(raw))
