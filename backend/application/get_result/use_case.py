from backend.application.errors import ResultNotFound
from backend.application.get_result.query import GetResultQuery
from backend.application.get_result.result import GetResultResult
from backend.application.ports.result_repository import ResultRepository


class GetResultUseCase:
    def __init__(self, result_repo: ResultRepository):
        self._res_repo = result_repo

    def execute(self, query: GetResultQuery) -> GetResultResult:
        res = self._res_repo.get(query.session_id)
        if not res:
            raise ResultNotFound(query.session_id)
        return GetResultResult(
            session_id=res.session_id,
            common_questions=res.common,
            different_questions=res.difference,
            score=res.score,
        )
