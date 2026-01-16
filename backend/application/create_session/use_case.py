from backend.application.errors import TopicNotFound
from backend.domain.session.entities import Session
from backend.domain.session.repository import SessionRepository
from backend.domain.session.value_objects import (
    ParticipantId,
    SessionId,
    TopicId,
    TopicVersion,
)
from backend.domain.topic.repository import TopicRepository


class CreateSessionUseCase:

    def __init__(
        self,
        session_repo: SessionRepository,
        topic_repo: TopicRepository,
    ):
        self._session_repo = session_repo
        self._topic_repo = topic_repo

    def execute(
        self,
        *,
        session_id: SessionId,
        topic_id: TopicId,
        topic_version: TopicVersion,
        creator_id: ParticipantId,
        created_at: int,
    ) -> None:
        topic = self._topic_repo.get(
            topic_id=topic_id,
            topic_version=topic_version,
        )
        if not topic:
            raise TopicNotFound
        session = Session(
            id=session_id,
            topic_id=topic.id,
            topic_version=topic.version,
            created_at=created_at,
        )
        session.join(creator_id)
        self._session_repo.save(session)
