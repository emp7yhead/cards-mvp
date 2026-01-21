from time import time
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from backend.app.dependencies import (
    get_answers_uc,
    get_create_session_uc,
    get_join_session_uc,
    get_submit_answers_uc,
)
from backend.application.create_session.command import CreateSessionCommand
from backend.application.create_session.use_case import CreateSessionUseCase
from backend.application.get_result.query import GetResultQuery
from backend.application.get_result.use_case import GetResultUseCase
from backend.application.join_session.command import JoinSessionCommand
from backend.application.join_session.use_case import JoinSessionUseCase
from backend.application.submit_answers.command import SubmitAnswersCommand
from backend.application.submit_answers.use_case import SubmitAnswersUseCase
from backend.domain.session.value_objects import (
    ParticipantId,
    Preference,
    QuestionId,
    SessionId,
    TopicId,
    TopicVersion,
)
from backend.interfaces.http.sessions.schemas import (
    CreateSessionResponse,
    CreateSessionTopicRequest,
    GetResultResponse,
    JoinSessionResponse,
    SubmitAnswersRequest,
    SubmitAnswersResponse,
)

router = APIRouter(prefix='/sessions', tags=['session'])

@router.post('/')
def create_session(
    payload: CreateSessionTopicRequest,
    uc: Annotated[CreateSessionUseCase, Depends(get_create_session_uc)],
) -> CreateSessionResponse:
    session_id: SessionId = SessionId.generate()
    participant_id: ParticipantId = ParticipantId.generate()

    cmd = CreateSessionCommand(
        session_id=session_id,
        topic_id=TopicId(payload.topic_id),
        topic_version=TopicVersion(payload.version),
        creator_id=participant_id,
        created_at=int(time()),
    )
    uc.execute(cmd)
    return CreateSessionResponse(
        session_id=session_id.value,
        participant_id=participant_id.value,
    )


@router.post('/{session_id}/join')
async def join_session(
    session_id: str,
    uc: Annotated[JoinSessionUseCase, Depends(get_join_session_uc)],
) -> JoinSessionResponse:
    participant_id = ParticipantId.generate()
    cmd = JoinSessionCommand(
        session_id=SessionId(session_id),
        participant_id=participant_id,
    )
    uc.execute(cmd)
    return JoinSessionResponse(
        session_id=session_id,
        participant_id=participant_id.value,
    )


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
            QuestionId(question): Preference(preference)
            for question, preference in payload.answers.items()
        },
    )
    res = uc.execute(cmd)
    return SubmitAnswersResponse(
        session_completed=res.session_completed,
    )


@router.get('/{session_id}/results')
def get_results(
    session_id: UUID,
    uc: Annotated[GetResultUseCase, Depends(get_answers_uc)],
) -> GetResultResponse:
    query = GetResultQuery(
        session_id=SessionId(str(session_id)),
    )
    res = uc.execute(query)
    return GetResultResponse(
            session_id=session_id,
            common_questions=[q.value for q in res.common_questions],
            different_questions=[q.value for q in res.different_questions],
            score=res.score,
        )
