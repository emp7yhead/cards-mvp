from backend.application.errors import TopicNotFound
from backend.application.get_topic.query import GetTopicQuery
from backend.domain.topic.entities import Topic
from backend.domain.topic.repository import TopicRepository
from backend.infrastructure.topics.redis.repository import TopicRedisRepository


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
        topic = self._redis.get(
            topic_id=query.topic_id,
            version=query.version,
        )
        if topic:
            return topic

        topic = self._yaml.get(
            topic_id=query.topic_id,
            version=query.version,
        )
        if not topic:
            raise TopicNotFound

        self._redis.save(topic)
        return topic
