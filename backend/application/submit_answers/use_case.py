import logging

from backend.application.errors import (
    InvalidQuestion,
    SessionNotFound,
    TopicNotFound,
)
from backend.application.ports.result_repository import ResultRepository
from backend.application.submit_answers.command import SubmitAnswersCommand
from backend.application.submit_answers.result import SubmitAnswersResult
from backend.domain.result.calculator import ResultCalculator
from backend.domain.session.repository import SessionRepository
from backend.domain.topic.entities import Topic
from backend.domain.topic.repository import TopicRepository

logger = logging.getLogger(__name__)


class SubmitAnswersUseCase:
    def __init__(
        self,
        session_repo: SessionRepository,
        calc: ResultCalculator,
        result_repo: ResultRepository,
        topic_repo: TopicRepository,
    ):
        self._session_repo = session_repo
        self._calc = calc
        self._result_repo = result_repo
        self._topic_repo = topic_repo

    def _assert_valid(self, topic, questions):
        for qid in questions:
            if not topic.has_question(qid):
                raise InvalidQuestion

    def execute(self, cmd: SubmitAnswersCommand):
        logger.info(
            'Submit answers started',
            extra={
                'session_id': cmd.session_id.value,
                'participant_id': cmd.participant_id.value,
            },
        )
        session = self._session_repo.get(cmd.session_id)
        if not session:
            raise SessionNotFound
        topic: Topic | None = self._topic_repo.get(
            session.topic_id,
            session.topic_version,
        )
        if not topic:
            logger.error(
                'Topic not found',
                extra={
                    'topic_id': session.topic_id.value,
                },
            )
            raise TopicNotFound
        self._assert_valid(topic, cmd.get_questions_ids())
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
            logger.info(
                'Session completed',
                extra={
                    'session_id': cmd.session_id.value,
                },
            )
        logger.info(
            'Submit answers finished',
            extra={
                'session_id': cmd.session_id.value,
                'participant_id': cmd.participant_id.value,
            },
        )
        return SubmitAnswersResult(
            session_completed=session.is_completed(),
        )
