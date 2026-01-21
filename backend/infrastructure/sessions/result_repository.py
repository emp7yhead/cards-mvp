from backend.application.errors import ServiceUnavailable
import logging

import orjson
from redis import RedisError

from backend.domain.result.entities import Result
from backend.domain.session.value_objects import SessionId
from backend.infrastructure.redis.client import get_client
from backend.infrastructure.sessions.serializers import (
    result_from_dict,
    result_to_dict,
)

logger = logging.getLogger(__name__)


class RedisResultRepository:

    def __init__(self):
        self._redis = get_client()

    def _key(self, session_id: SessionId) -> str:
        return f"result:{session_id.value}"

    def save(self, result: Result) -> None:
        key = self._key(result.session_id)
        try:
            self._redis.set(
                key,
                orjson.dumps(result_to_dict(result)),
            )
        except RedisError as e:
            logger.error(
                "Failed to save session results: %s", e,
                extra={
                    'session_id': result.session_id.value,
                },
            )
            raise ServiceUnavailable from e

    def get(self, session_id: SessionId) -> Result | None:
        try:
            raw = self._redis.get(self._key(session_id))
        except RedisError as e:
            logger.error(
                "Failed to get session results: %s", e,
                extra={
                    'session_id': session_id.value,
                },
            )
            raise ServiceUnavailable from e
        if not raw:
            return None
        return result_from_dict(orjson.loads(raw))
