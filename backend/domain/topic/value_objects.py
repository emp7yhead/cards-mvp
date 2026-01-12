from dataclasses import dataclass


@dataclass(frozen=True)
class TopicId:
    value: str


@dataclass(frozen=True)
class TopicVersion:
    value: str


@dataclass(frozen=True)
class QuestionId:
    value: str
