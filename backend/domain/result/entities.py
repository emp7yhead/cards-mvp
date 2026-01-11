from dataclasses import dataclass

from backend.domain.session.value_objects import SessionId


@dataclass(frozen=True)
class Result:
    session_id: SessionId
    score: int
    common: list[str]
    difference: list[str]
