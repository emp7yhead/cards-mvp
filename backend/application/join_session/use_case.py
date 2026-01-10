from backend.application.errors import SessionNotFound
from backend.application.join_session.command import JoinSessionCommand
from backend.domain.session.repository import SessionRepository


class JoinSessionUseCase:

    def __init__(self, session_repo: SessionRepository):
        self._session_repo = session_repo

    def execute(
        self,
        cmd: JoinSessionCommand,
    ) -> None:
        session = self._session_repo.get(cmd.session_id)
        if not session:
            raise SessionNotFound
        session.join(cmd.participant_id)
        self._session_repo.save(session)
