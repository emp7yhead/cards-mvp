from dataclasses import dataclass, field
from enum import StrEnum

from backend.domain.session.errors import (
    ParticipantAlreadyAnswered,
    SessionCompleted,
    SessionExpired,
    TooManyParticipants,
    UnknownParticipant,
)
from backend.domain.session.value_objects import (
    ParticipantId,
    SessionId,
    TopicId,
)

PARTICIPANTS_LIMIT = 2

class SessionState(StrEnum):
    WAITING = 'waiting'
    COMPLETED = 'completed'
    EXPIRED = 'expired'


@dataclass
class Session:
    id: SessionId
    topic: TopicId
    topics_version: int
    created_at: int
    state: SessionState = SessionState.WAITING
    participants: dict[ParticipantId, dict] = field(default_factory=dict)

    def _assert_active(self):
        if self.state == SessionState.COMPLETED:
            raise SessionCompleted
        if self.state == SessionState.EXPIRED:
            raise SessionExpired

    def _assert_participants_limit(self):
        if len(self.participants) >= PARTICIPANTS_LIMIT:
            raise TooManyParticipants

    def _all_answered(self) -> bool:
        if len(self.participants) < PARTICIPANTS_LIMIT:
            return False
        return all(
            len(answer) > 0
            for answer in self.participants.values()
        )

    def expire(self):
        self.state = SessionState.EXPIRED

    def join(self, participant_id: ParticipantId):
        self._assert_active()
        if participant_id in self.participants:
            return None
        self._assert_participants_limit()
        self.participants[participant_id] = {}

    def submit_answers(
        self,
        participant_id: ParticipantId,
        answers: dict,
    ):
        self._assert_active()
        if participant_id not in self.participants:
            raise UnknownParticipant
        if self.participants[participant_id]:
            raise ParticipantAlreadyAnswered
        self.participants[participant_id] = answers
        if self._all_answered():
            self.state = SessionState.COMPLETED

