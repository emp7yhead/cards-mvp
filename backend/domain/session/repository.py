from typing import Protocol

from backend.domain.session.entities import Session
from backend.domain.session.value_objects import SessionId


class SessionRepository(Protocol):
    def save(self, session: Session):...
    def get(self, session_id: SessionId) -> Session | None:...
