from backend.application.errors import SessionNotFound
from backend.application.ports.result_repository import ResultRepository
from backend.application.submit_answers.command import SubmitAnswersCommand
from backend.application.submit_answers.result import SubmitAnswersResult
from backend.domain.result.calculator import ResultCalculator
from backend.domain.session.repository import SessionRepository


class SubmitAnswersUseCase:
    def __init__(
        self,
        session_repo: SessionRepository,
        calc: ResultCalculator,
        result_repo: ResultRepository,
    ):
        self._session_repo = session_repo
        self._calc = calc
        self._result_repo = result_repo

    def execute(self, cmd: SubmitAnswersCommand):
        session = self._session_repo.get(cmd.session_id)
        if not session:
            raise SessionNotFound
        session.submit_answers(
            participant_id=cmd.participant_id,
            answers=cmd.answers,
        )
        self._session_repo.save(session)
        if session.is_completed():
            result = self._calc.calculate(
                session.id,
                *session.participants.values(),
            )
            self._result_repo.save(result)
        return SubmitAnswersResult(
            session_completed=session.is_completed(),
        )
