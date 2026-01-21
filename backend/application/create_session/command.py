from pydantic import BaseModel

from backend.domain.session.value_objects import (
    ParticipantId,
    SessionId,
    TopicId,
    TopicVersion,
)


class CreateSessionCommand(BaseModel):
    session_id: SessionId
    topic_id: TopicId
    topic_version: TopicVersion
    creator_id: ParticipantId
    created_at: int
