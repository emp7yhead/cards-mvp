from backend.application.errors import SessionNotFound
from backend.application.submit_answers.command import SubmitAnswersCommand
from backend.application.submit_answers.result import SubmitAnswersResult
from backend.domain.session.repository import SessionRepository


class SubmitAnswersUseCase:
    def __init__(self, session_repo: SessionRepository):
        self._session_repo = session_repo

    def execute(self, cmd: SubmitAnswersCommand):
        session = self._session_repo.get(cmd.session_id)
        if not session:
            raise SessionNotFound
        session.submit_answers(
            participant_id=cmd.participant_id,
            answers=cmd.answers,
        )
        self._session_repo.save(session)
        return SubmitAnswersResult(
            session_completed=session.is_completed(),
        )
