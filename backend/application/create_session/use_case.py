import logging

from backend.application.create_session.command import CreateSessionCommand
from backend.application.errors import TopicNotFound
from backend.domain.session.entities import Session
from backend.domain.session.repository import SessionRepository
from backend.domain.topic.repository import TopicRepository

logger = logging.getLogger(__name__)


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
        cmd: CreateSessionCommand,
    ) -> None:
        logger.info(
            'Create session started',
            extra={
                'session_id': cmd.session_id.value,
                'topic_id': cmd.topic_id.value,
            },
        )
        topic = self._topic_repo.get(
            topic_id=cmd.topic_id,
            topic_version=cmd.topic_version,
        )
        if not topic:
            logger.error(
                'Topic not found',
                extra={
                    'topic_id': cmd.topic_id.value,
                },
            )
            raise TopicNotFound
        session = Session(
            id=cmd.session_id,
            topic_id=topic.id,
            topic_version=topic.version,
            created_at=cmd.created_at,
        )
        session.join(cmd.creator_id)
        self._session_repo.save(session)
        logger.info(
            'Create session finished',
            extra={
                'session_id': cmd.session_id.value,
                'topic_id': cmd.topic_id.value,
            },
        )
