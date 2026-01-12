from dataclasses import dataclass

from backend.domain.topic.value_objects import QuestionId, TopicId, TopicVersion


@dataclass(frozen=True)
class Topic:
    id: TopicId
    version: TopicVersion
    questions: tuple[QuestionId, ...]

    def has_question(self, question_id):
        return question_id in self.questions
