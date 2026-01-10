import enum
from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class SessionId:
    value: str

    @staticmethod
    def generate() -> 'SessionId':
        return SessionId(str(uuid4()))

    def __post_init__(self):
        if not self.value:
            raise ValueError('SessionId cannot be empty')



@dataclass(frozen=True)
class TopicId:
    value: str


@dataclass(frozen=True)
class ParticipantId:
    value: str

    @staticmethod
    def generate() -> 'ParticipantId':
        return ParticipantId(str(uuid4()))

    def __post_init__(self):
        if not self.value:
            raise ValueError('ParticipantId cannot be empty')


@dataclass(frozen=True)
class QuestionId:
    value: str


class SessionState(enum.StrEnum):
    WAITING = 'waiting'
    COMPLETED = 'completed'
    EXPIRED = 'expired'


class Preference(enum.StrEnum):
    LIKE = 'like'
    DISLIKE = 'dislike'
    NEUTRAL = 'neutral'


Answers = dict[QuestionId, Preference]
