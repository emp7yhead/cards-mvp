from dataclasses import dataclass, field

from backend.domain.session.errors import (
    ParticipantAlreadyAnswered,
    SessionCompleted,
    SessionExpired,
    TooManyParticipants,
    UnknownParticipant,
)
from backend.domain.session.value_objects import (
    ParticipantId,
    Preference,
    SessionId,
    SessionState,
    TopicId,
    TopicVersion,
)

PARTICIPANTS_LIMIT = 2


@dataclass
class Session:
    id: SessionId
    topic_id: TopicId
    topic_version: TopicVersion
    created_at: int
    state: SessionState = SessionState.WAITING
    participants: dict[ParticipantId, dict] = field(default_factory=dict)

    @classmethod
    def restore(
        cls,
        *,
        session_id: SessionId,
        topic_id: TopicId,
        topic_version: TopicVersion,
        created_at: int,
        state: SessionState,
        participants: dict[ParticipantId, dict[str, Preference]],
    ) -> 'Session':
        session = cls.__new__(cls)

        session.id = session_id
        session.topic_id = topic_id
        session.topic_version = topic_version
        session.created_at = created_at
        session.state = state
        session.participants = participants

        return session

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
        if self.state == SessionState.COMPLETED:
            return None
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

    def is_completed(self):
        return self.state == SessionState.COMPLETED

