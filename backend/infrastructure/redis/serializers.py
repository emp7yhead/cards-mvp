from backend.domain.result.entities import Result
from backend.domain.session.entities import Session
from backend.domain.session.value_objects import (
    ParticipantId,
    Preference,
    SessionId,
    TopicId,
)


def session_to_dict(session: Session) -> dict:
    payload = {
        "session_id": session.id.value,
        "topic": session.topic.value,
        "topics_version": session.topics_version,
        "created_at": session.created_at,
        "state": session.state,
        "participants": {
            pid.value: {
                key: pref.name
                for key, pref in answers.items()
            }
            for pid, answers in session.participants.items()
        },
    }

    return payload


def session_from_dict(data: dict) -> Session:
    session = Session.restore(
        session_id = SessionId(data['session_id']),
        topic = TopicId(data['topic']),
        topics_version = data['topics_version'],
        created_at = data['created_at'],
        state = data['state'],
        participants = {
            ParticipantId(k): {
                q: Preference[p] for q, p in v.items()
            } for k, v in data['participants'].items()
        },
    )
    return session


def result_to_dict(result: Result) -> dict:
    return {
        "session_id": result.session_id.value,
        "common_questions": result.common,
        "difference_questions": result.difference,
        "score": result.score,
    }


def result_from_dict(data: dict) -> Result:
    return Result(
        session_id=SessionId(data["session_id"]),
        common=data["common_questions"],
        difference=data["difference_questions"],
        score=data["score"],
    )
