from dataclasses import dataclass

from backend.domain.session.value_objects import (
    Answers,
    ParticipantId,
    SessionId,
)


@dataclass(frozen=True)
class SubmitAnswersCommand:
    session_id: SessionId
    participant_id: ParticipantId
    answers: Answers
