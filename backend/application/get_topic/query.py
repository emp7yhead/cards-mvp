from dataclasses import dataclass

from backend.domain.topic.value_objects import TopicId, TopicVersion


@dataclass(frozen=True)
class GetTopicQuery:
    topic_id: TopicId
    version: TopicVersion
