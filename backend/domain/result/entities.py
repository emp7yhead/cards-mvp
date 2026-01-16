from dataclasses import dataclass

from backend.domain.session.value_objects import SessionId
from backend.domain.topic.value_objects import QuestionId


@dataclass(frozen=True)
class Result:
    session_id: SessionId
    score: int
    common: list[QuestionId]
    difference: list[QuestionId]
