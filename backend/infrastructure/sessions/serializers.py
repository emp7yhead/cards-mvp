from backend.domain.result.entities import Result
from backend.domain.session.entities import Session
from backend.domain.session.value_objects import (
    ParticipantId,
    Preference,
    SessionId,
    TopicId,
    TopicVersion,
)
from backend.domain.topic.value_objects import QuestionId


def session_to_dict(session: Session) -> dict:
    payload = {
        "session_id": session.id.value,
        "topic_id": session.topic_id.value,
        "topic_version": session.topic_version.value,
        "created_at": session.created_at,
        "state": session.state,
        "participants": {
            pid.value: {
                key.value: pref.name
                for key, pref in answers.items()
            }
            for pid, answers in session.participants.items()
        },
    }

    return payload


def session_from_dict(data: dict) -> Session:
    session = Session.restore(
        session_id = SessionId(data['session_id']),
        topic_id = TopicId(data['topic_id']),
        topic_version = TopicVersion(data['topic_version']),
        created_at = data['created_at'],
        state = data['state'],
        participants = {
            ParticipantId(k): {
                QuestionId(q): Preference[p] for q, p in v.items()
            } for k, v in data['participants'].items()
        },
    )
    return session


def result_to_dict(result: Result) -> dict:
    return {
        "session_id": result.session_id.value,
        "common_questions": [r.value for r in result.common],
        "difference_questions": [r.value for r in result.difference],
        "score": result.score,
    }


def result_from_dict(data: dict) -> Result:
    return Result(
        session_id=SessionId(data["session_id"]),
        common=[QuestionId(qid) for qid in data["common_questions"]],
        difference=[QuestionId(qid) for qid in data["difference_questions"]],
        score=data["score"],
    )
