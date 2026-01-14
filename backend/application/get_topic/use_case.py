import logging

from redis.exceptions import RedisError

from backend.application.errors import TopicNotFound
from backend.application.get_topic.query import GetTopicQuery
from backend.domain.topic.entities import Topic
from backend.domain.topic.repository import TopicRepository
from backend.infrastructure.topics.redis.repository import TopicRedisRepository

logger = logging.getLogger(__name__)

class GetTopicUseCase:

    def __init__(
        self,
        yaml_repo: TopicRepository,
        redis_repo: TopicRedisRepository,
    ):
        self._yaml = yaml_repo
        self._redis = redis_repo

    def execute(
        self,
        query: GetTopicQuery,
    ) -> Topic:
        try:
            topic = self._redis.get(
                topic_id=query.topic_id,
                version=query.version,
            )
        except RedisError as e:
            logger.error("Error while get topic from cache: %s", e)
        if topic:
            return topic

        topic = self._yaml.get(
            topic_id=query.topic_id,
            version=query.version,
        )
        if not topic:
            raise TopicNotFound
        try:
            self._redis.save(topic)
        except RedisError as e:
            logger.error("Error while save topic to cache: %s", e)
        return topic
