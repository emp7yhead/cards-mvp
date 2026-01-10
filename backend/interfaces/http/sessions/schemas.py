from uuid import UUID

from pydantic import BaseModel


class SubmitAnswersRequest(BaseModel):
    participant_id: UUID
    answers: dict[str, str]


class SubmitAnswersResponse(BaseModel):
    session_completed: bool


class GetResultResponse(BaseModel):
    session_id: UUID
    common_questions: list[str]
    different_questions: list[str]
    score: int
