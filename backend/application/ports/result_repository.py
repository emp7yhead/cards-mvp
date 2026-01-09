from typing import Protocol

from backend.domain.result.entities import Result
from backend.domain.session.value_objects import SessionId


class ResultRepository(Protocol):
    def save(self, result: Result): ...
    def get(self, session_id: SessionId) -> Result | None: ...
