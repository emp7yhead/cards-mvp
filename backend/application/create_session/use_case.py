from backend.domain.session.entities import Session
from backend.domain.session.repository import SessionRepository
from backend.domain.session.value_objects import (
    ParticipantId,
    SessionId,
    TopicId,
)


class CreateSessionUseCase:

    def __init__(self, session_repo: SessionRepository):
        self._session_repo = session_repo

    def execute(
        self,
        *,
        session_id: SessionId,
        topic: TopicId,
        topics_version: int,
        creator_id: ParticipantId,
        created_at: int,
    ) -> None:
        session = Session(
            id=session_id,
            topic=topic,
            topics_version=topics_version,
            created_at=created_at,
        )
        session.join(creator_id)
        self._session_repo.save(session)
