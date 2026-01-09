import enum
from dataclasses import dataclass


@dataclass(frozen=True)
class SessionId:
    value: str


@dataclass(frozen=True)
class TopicId:
    value: str


@dataclass(frozen=True)
class ParticipantId:
    value: str


class SessionState(enum.StrEnum):
    WAITING = 'waiting'
    COMPLETED = 'completed'
    EXPIRED = 'expired'


class Preference(enum.StrEnum):
    LIKE = 'like'
    DISLIKE = 'dislike'
    NEUTRAL = 'neutral'
