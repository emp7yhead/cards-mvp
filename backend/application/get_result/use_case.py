import logging

from backend.application.errors import ResultNotFound
from backend.application.get_result.query import GetResultQuery
from backend.application.get_result.result import GetResultResult
from backend.application.ports.result_repository import ResultRepository

logger = logging.getLogger(__name__)

class GetResultUseCase:
    def __init__(self, result_repo: ResultRepository):
        self._res_repo = result_repo

    def execute(self, query: GetResultQuery) -> GetResultResult:
        logger.info(
            "Get result started",
            extra={
                "session_id": query.session_id.value,
                "topic_id": query.topic_id.value,
            },
        )
        res = self._res_repo.get(query.session_id)
        if not res:
            logger.info(
                'Result for session %s not found', query.session_id.value,
                extra={'session_id': query.session_id.value},
            )
            raise ResultNotFound(query.session_id)
        logger.info(
            "Get result finished",
            extra={
                "session_id": query.session_id.value,
                "topic_id": query.topic_id.value,
            },
        )
        return GetResultResult(
            session_id=res.session_id,
            common_questions=res.common,
            different_questions=res.difference,
            score=res.score,
        )
