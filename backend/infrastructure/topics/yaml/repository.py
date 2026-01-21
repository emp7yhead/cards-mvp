from pathlib import Path

import yaml

from backend.domain.topic.entities import Topic
from backend.domain.topic.repository import TopicRepository
from backend.domain.topic.value_objects import TopicId, TopicVersion
from backend.infrastructure.topics.yaml.serializers import TopicYamlSerializer


class TopicYamlRepository(TopicRepository):

    def __init__(self, base_path: Path):
        self._base_path = base_path

    def list_all(self) -> list[Topic]:
        topics = []

        for path in self._base_path.glob('*.yaml'):
            with open(path) as f:
                data = yaml.safe_load(f)
                topics.append(TopicYamlSerializer.loads(data))

        return topics

    def get(
        self,
        topic_id: TopicId,
        topic_version: TopicVersion | None = None,
    ) -> Topic | None:
        path = self._base_path / f'{topic_id.value}.yaml'

        if not path.exists():
            return None

        with open(path, encoding='utf-8') as f:
            data = yaml.safe_load(f)

        topic = TopicYamlSerializer.loads(data)

        if topic_version.value and topic.version != topic_version:
            return None

        return topic
