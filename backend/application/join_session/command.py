from pydantic import BaseModel

from backend.domain.session.value_objects import ParticipantId, SessionId


class JoinSessionCommand(BaseModel):
    session_id: SessionId
    participant_id: ParticipantId
