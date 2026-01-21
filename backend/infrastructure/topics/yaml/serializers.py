from backend.domain.topic.entities import Topic
from backend.domain.topic.value_objects import QuestionId, TopicId, TopicVersion


class TopicYamlSerializer:

    @staticmethod
    def loads(data: dict) -> Topic:
        return Topic(
            id=TopicId(data['id']),
            version=TopicVersion(data['version']),
            questions=tuple(
                QuestionId(q) for q in data['questions']
            ),
        )
