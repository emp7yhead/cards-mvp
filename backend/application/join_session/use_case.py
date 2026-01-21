import logging

from backend.application.errors import SessionNotFound
from backend.application.join_session.command import JoinSessionCommand
from backend.domain.session.repository import SessionRepository

logger = logging.getLogger(__name__)


class JoinSessionUseCase:

    def __init__(self, session_repo: SessionRepository):
        self._session_repo = session_repo

    def execute(
        self,
        cmd: JoinSessionCommand,
    ) -> None:
        logger.info(
            'Join session started',
            extra={
                'session_id': cmd.session_id.value,
                'participant_id': cmd.participant_id.value,
            },
        )
        session = self._session_repo.get(cmd.session_id)
        if not session:
            raise SessionNotFound
        session.join(cmd.participant_id)
        self._session_repo.save(session)
        logger.info(
            'Join session finished',
            extra={
                'session_id': cmd.session_id.value,
                'participant_id': cmd.participant_id.value,
            },
        )
