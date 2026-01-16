from pathlib import Path

from backend.application.create_session.use_case import CreateSessionUseCase
from backend.application.get_result.use_case import GetResultUseCase
from backend.application.get_topic.prewarm_use_case import PrewarmTopicsUseCase
from backend.application.get_topic.use_case import GetTopicUseCase
from backend.application.join_session.use_case import JoinSessionUseCase
from backend.application.submit_answers.use_case import SubmitAnswersUseCase
from backend.infrastructure.redis.result_repository import RedisResultRepository
from backend.infrastructure.redis.sessions_repository import (
    RedisSessionRepository,
)
from backend.infrastructure.topics.redis.repository import TopicRedisRepository
from backend.infrastructure.topics.yaml.repository import TopicYamlRepository

BASE_PATH = Path(__file__).resolve().parent.parent.parent / 'topics_example'


class Container:
    session_repo: RedisSessionRepository | None = None
    result_repo: RedisResultRepository | None = None
    topic_yaml_repo: TopicYamlRepository | None = None
    topic_redis_repo: TopicRedisRepository | None = None

    submit_answers_uc: SubmitAnswersUseCase | None = None
    get_answers_uc: GetResultUseCase | None = None
    create_session_uc: CreateSessionUseCase | None = None
    join_session_uc: JoinSessionUseCase | None = None
    get_topic_uc: GetTopicUseCase | None = None
    prewarm_topic_uc: PrewarmTopicsUseCase | None = None

container = Container()
