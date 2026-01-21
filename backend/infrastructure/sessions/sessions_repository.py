from backend.application.errors import ServiceUnavailable
import logging

import orjson
from redis import RedisError

from backend.domain.session.entities import Session
from backend.domain.session.value_objects import SessionId
from backend.infrastructure.redis.client import get_client
from backend.infrastructure.sessions.serializers import (
    session_from_dict,
    session_to_dict,
)

logger = logging.getLogger(__name__)

SESSION_TTL_SECONDS = 60 * 60 * 24


class RedisSessionRepository:

    def __init__(self):
        self._redis = get_client()

    def _key(self, session_id: SessionId) -> str:
        return f"session:{session_id.value}"

    def get(self, session_id: SessionId) -> Session | None:
        try:
            raw = self._redis.get(self._key(session_id))
        except RedisError as e:
            logger.error(
                "Failed to get session: %s", e,
                extra={
                    'session_id': session_id.value,
                },
            )
            raise ServiceUnavailable from e
        if not raw:
            return None
        return session_from_dict(orjson.loads(raw))

    def save(self, session: Session) -> None:
        key = self._key(session.id)
        data = orjson.dumps(session_to_dict(session))
        try:
            self._redis.set(
                key,
                data,
                ex=SESSION_TTL_SECONDS,
            )
        except RedisError as e:
            logger.error(
                "Failed to save session: %s", e,
                extra={
                    'session_id': session.id,
                },
            )
            raise ServiceUnavailable from e
