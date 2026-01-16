from backend.domain.topic.entities import Topic
from backend.domain.topic.repository import TopicRepository
from backend.domain.topic.value_objects import TopicId, TopicVersion
from backend.infrastructure.redis.client import get_client
from backend.infrastructure.topics.redis.serializers import TopicRedisSerializer


class TopicRedisRepository(TopicRepository):

    def __init__(self, ttl_seconds: int = 3600):
        self._redis = get_client()
        self._ttl = ttl_seconds

    def _key(self, topic_id: TopicId, version: TopicVersion) -> str:
        return f"topic:{topic_id.value}:{version.value}"

    def get(
        self,
        topic_id: TopicId,
        topic_version: TopicVersion | None = None,
    ) -> Topic | None:
        if topic_version is None:
            return None

        raw = self._redis.get(self._key(topic_id, topic_version))
        if not raw:
            return None

        return TopicRedisSerializer.loads(raw)

    def save(self, topic: Topic) -> None:
        self._redis.set(
            self._key(topic.id, topic.version),
            TopicRedisSerializer.dumps(topic),
            ex=self._ttl,
        )
