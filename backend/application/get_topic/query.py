from dataclasses import dataclass

from backend.domain.topic.value_objects import TopicId


@dataclass(frozen=True)
class GetTopicQuery:
    topic_id: TopicId
