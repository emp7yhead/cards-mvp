import orjson

from backend.domain.topic.entities import Topic
from backend.domain.topic.value_objects import QuestionId, TopicId, TopicVersion


class TopicRedisSerializer:

    @staticmethod
    def dumps(topic: Topic) -> bytes:
        return orjson.dumps({
            "id": topic.id.value,
            "version": topic.version.value,
            "questions": [q.value for q in topic.questions],
        })

    @staticmethod
    def loads(raw: bytes) -> Topic:
        data = orjson.loads(raw)

        return Topic(
            id=TopicId(data["id"]),
            version=TopicVersion(data["version"]),
            questions=tuple(
                QuestionId(q) for q in data["questions"]
            ),
        )
