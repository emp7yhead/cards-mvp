import logging

from redis.exceptions import RedisError

from backend.domain.topic.repository import TopicRepository
from backend.infrastructure.topics.redis.repository import TopicRedisRepository

logger = logging.getLogger(__name__)


class PrewarmTopicsUseCase:

    def __init__(
        self,
        yaml_repo: TopicRepository,
        redis_repo: TopicRedisRepository,
    ):
        self._yaml = yaml_repo
        self._redis = redis_repo

    async def execute(self) -> None:
        topics = self._yaml.list_all()

        for topic in topics:
            try:
                self._redis.save(topic)
            except RedisError as e:
                logger.error('Error while prewarm cache: %s', str(e))
