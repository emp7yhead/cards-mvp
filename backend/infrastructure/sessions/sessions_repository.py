import orjson

from backend.domain.session.entities import Session
from backend.domain.session.value_objects import SessionId
from backend.infrastructure.redis.client import get_client
from backend.infrastructure.sessions.serializers import (
    session_from_dict,
    session_to_dict,
)

SESSION_TTL_SECONDS = 60 * 60 * 24


class RedisSessionRepository:

    def __init__(self):
        self._redis = get_client()

    def _key(self, session_id: SessionId) -> str:
        return f"session:{session_id.value}"

    def get(self, session_id: SessionId) -> Session | None:
        raw = self._redis.get(self._key(session_id))
        if not raw:
            return None
        return session_from_dict(orjson.loads(raw))

    def save(self, session: Session) -> None:
        key = self._key(session.id)
        data = orjson.dumps(session_to_dict(session))
        self._redis.set(
            key,
            data,
            ex=SESSION_TTL_SECONDS,
        )
