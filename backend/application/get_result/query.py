from dataclasses import dataclass

from backend.domain.session.value_objects import SessionId


@dataclass(frozen=True)
class GetResultQuery:
    session_id: SessionId
