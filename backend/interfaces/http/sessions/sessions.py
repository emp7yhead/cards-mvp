from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from backend.app.dependencies import get_get_answers_uc, get_submit_answers_uc
from backend.application.errors import ResultNotFound, SessionNotFound
from backend.application.get_result.query import GetResultQuery
from backend.application.get_result.use_case import GetResultUseCase
from backend.application.submit_answers.command import SubmitAnswersCommand
from backend.application.submit_answers.use_case import SubmitAnswersUseCase
from backend.domain.session.errors import SessionCompleted, UnknownParticipant
from backend.domain.session.value_objects import (
    ParticipantId,
    Preference,
    SessionId,
)
from backend.interfaces.http.sessions.schemas import (
    GetResultResponse,
    SubmitAnswersRequest,
    SubmitAnswersResponse,
)

router = APIRouter(prefix='/sessions', tags=['session'])


@router.post('/{session_id}/answers')
def submit_answers(
    session_id: UUID,
    payload: SubmitAnswersRequest,
    uc: Annotated[SubmitAnswersUseCase, Depends(get_submit_answers_uc)],
) -> SubmitAnswersResponse:
    cmd = SubmitAnswersCommand(
        session_id=SessionId(str(session_id)),
        participant_id=ParticipantId(str(payload.participant_id)),
        answers={
            question: Preference(preference)
            for question, preference in payload.answers.items()
        },
    )
    try:
        res = uc.execute(cmd)
    except SessionCompleted as e:
        raise HTTPException(
            status_code=409,
            detail='Session alredy completed',
        ) from e
    except UnknownParticipant as e:
        raise HTTPException(
            status_code=404,
            detail='Unknown participant',
        ) from e
    except SessionNotFound as e:
        raise HTTPException(
            status_code=404,
            detail='Session not found',
        ) from e
    return SubmitAnswersResponse(
        session_completed=res.session_completed,
    )


@router.get('/{session_id}/results')
def get_results(
    session_id: UUID,
    uc: Annotated[GetResultUseCase, Depends(get_get_answers_uc)],
) -> GetResultResponse:
    query = GetResultQuery(
        session_id=session_id,
    )
    try:
        res = uc.execute(query)
    except ResultNotFound as e:
        raise HTTPException(
            status_code=404,
            detail='Results not found',
        ) from e
    return GetResultResponse(
            session_id=session_id,
            common_questions=res.common_questions,
            different_questions=res.different_questions,
            score=res.score,
        )
