from backend.domain.result.entities import Result
from backend.domain.session.entities import Session
from backend.domain.session.value_objects import Preference


def session_to_dict(session: Session) -> dict:
    return {
        "id": session.id.value,
        "participants": list(session.participants),
        "answers": {
            pid: {
                qid: pref.value
                for qid, pref in answers.items()
            }
            for pid, answers in session.answers.items()
        },
        "completed": session.is_completed(),
    }


def session_from_dict(data: dict) -> Session:
    session = Session.restore(
        session_id=data["id"],
        participants=data["participants"],
    )
    for pid, answers in data["answers"].items():
        session.submit_answers(
            pid,
            {
                question: Preference(preference)
                for question, preference
                in answers.items()
            },
        )
    return session


def result_to_dict(result: Result) -> dict:
    return {
        "session_id": result.session_id.value,
        "common_questions": result.common_questions,
        "score": result.score,
    }


def result_from_dict(data: dict) -> Result:
    return Result(
        session_id=data["session_id"],
        common_questions=data["common_questions"],
        score=data["score"],
    )
