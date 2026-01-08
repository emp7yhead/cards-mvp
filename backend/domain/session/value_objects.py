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

