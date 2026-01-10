from datetime import datetime

import pytest

from backend.domain.session.entities import (
    PARTICIPANTS_LIMIT,
    Session,
)
from backend.domain.session.errors import (
    ParticipantAlreadyAnswered,
    SessionCompleted,
    SessionExpired,
    TooManyParticipants,
    UnknownParticipant,
)
from backend.domain.session.value_objects import ParticipantId, SessionState

TEST_PARTICIPANT_1 = ParticipantId('biba')
TEST_PARTICIPANT_2 = ParticipantId('boba')
TEST_PARTICIPANT_3 = ParticipantId('buba')

@pytest.fixture
def test_session():
    return Session(
        id='test',
        topic='test',
        topics_version=datetime.now(),
        created_at=datetime.now(),
    )


@pytest.fixture
def full_session(test_session):
    test_session.join(TEST_PARTICIPANT_1)
    test_session.join(TEST_PARTICIPANT_2)
    return test_session


def test_expired_session(test_session):
    test_session.expire()
    assert test_session.state == SessionState.EXPIRED
    with pytest.raises(SessionExpired):
        test_session.join(TEST_PARTICIPANT_1)


def test_session_join(full_session):
    assert TEST_PARTICIPANT_1 in full_session.participants.keys()
    assert TEST_PARTICIPANT_2 in full_session.participants.keys()
    full_session.join(TEST_PARTICIPANT_1)
    full_session.join(TEST_PARTICIPANT_2)
    assert len(full_session.participants.keys()) == PARTICIPANTS_LIMIT


def test_session_negative_join(full_session):
    with pytest.raises(TooManyParticipants):
        full_session.join(TEST_PARTICIPANT_3)


def test_session_participants_answers(full_session):
    with pytest.raises(UnknownParticipant):
        full_session.submit_answers(TEST_PARTICIPANT_3, {'a': 1})
    full_session.submit_answers(TEST_PARTICIPANT_1, {'a': 1})
    with pytest.raises(ParticipantAlreadyAnswered):
        full_session.submit_answers(TEST_PARTICIPANT_1, {'a': 1})
    full_session.submit_answers(TEST_PARTICIPANT_2, {'a': 1})
    assert full_session.state == SessionState.COMPLETED
    with pytest.raises(SessionCompleted):
        full_session.submit_answers(TEST_PARTICIPANT_2, {'a': 1})

