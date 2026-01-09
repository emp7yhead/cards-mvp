from dataclasses import dataclass

from backend.domain.session.value_objects import QuestionId, SessionId


@dataclass(frozen=True)
class GetResultResult:
    session_id: SessionId
    common_questions: list[QuestionId]
    different_questions: list[QuestionId]
    score: int
