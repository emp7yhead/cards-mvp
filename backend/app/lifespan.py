from contextlib import asynccontextmanager

from fastapi.applications import FastAPI

from backend.app.container import BASE_PATH, container
from backend.application.create_session.use_case import CreateSessionUseCase
from backend.application.get_result.use_case import GetResultUseCase
from backend.application.get_topic.prewarm_use_case import PrewarmTopicsUseCase
from backend.application.get_topic.use_case import GetTopicUseCase
from backend.application.join_session.use_case import JoinSessionUseCase
from backend.application.submit_answers.use_case import SubmitAnswersUseCase
from backend.domain.result.calculator import SimpleResultsCalculator
from backend.infrastructure.redis.result_repository import RedisResultRepository
from backend.infrastructure.redis.sessions_repository import (
    RedisSessionRepository,
)
from backend.infrastructure.topics.redis.repository import TopicRedisRepository
from backend.infrastructure.topics.yaml.repository import TopicYamlRepository


async def init_container(app: FastAPI):
    container.session_repo = RedisSessionRepository()
    container.result_repo = RedisResultRepository()

    container.topic_yaml_repo = TopicYamlRepository(BASE_PATH)
    container.topic_redis_repo = TopicRedisRepository()

    container.submit_answers_uc = SubmitAnswersUseCase(
        session_repo=container.session_repo,
        calc=SimpleResultsCalculator(),
        result_repo=container.result_repo,
        topic_repo=container.topic_redis_repo,
    )

    container.get_answers_uc = GetResultUseCase(container.result_repo)
    container.create_session_uc = CreateSessionUseCase(container.session_repo)
    container.join_session_uc = JoinSessionUseCase(container.session_repo)

    container.get_topic_uc = GetTopicUseCase(
        container.topic_yaml_repo,
        container.topic_redis_repo,
    )

    container.prewarm_topic_uc = PrewarmTopicsUseCase(
        container.topic_yaml_repo,
        container.topic_redis_repo,
    )

    await container.prewarm_topic_uc.execute()


async def shutdown_container(app: FastAPI): ...


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_container(app)
    yield
    await shutdown_container(app)
