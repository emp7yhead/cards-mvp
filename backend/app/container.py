from backend.application.create_session.use_case import CreateSessionUseCase
from backend.application.get_result.use_case import GetResultUseCase
from backend.application.join_session.use_case import JoinSessionUseCase
from backend.application.submit_answers.use_case import SubmitAnswersUseCase
from backend.domain.result.calculator import SimpleResultsCalculator
from backend.infrastructure.redis.result_repository import RedisResultRepository
from backend.infrastructure.redis.sessions_repository import (
    RedisSessionRepository,
)

session_repo = RedisSessionRepository()
result_repo = RedisResultRepository()

result_calc = SimpleResultsCalculator()

submit_answers_uc = SubmitAnswersUseCase(
    session_repo=session_repo,
    calc=result_calc,
    result_repo=result_repo,
)

get_answers_uc = GetResultUseCase(
    result_repo=result_repo,
)

create_session_uc = CreateSessionUseCase(session_repo=session_repo)

join_session_uc = JoinSessionUseCase(session_repo=session_repo)
