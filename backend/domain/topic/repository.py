from typing import Protocol

from backend.domain.topic.entities import Topic
from backend.domain.topic.value_objects import TopicId, TopicVersion


class TopicRepository(Protocol):
    def get(
        self,
        topic_id: TopicId,
        topic_version: TopicVersion | None = None,
    ) -> Topic | None: ...
