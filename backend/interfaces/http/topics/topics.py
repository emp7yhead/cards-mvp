from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from backend.app.dependencies import get_get_topic_uc
from backend.application.errors import TopicNotFound
from backend.application.get_topic.query import GetTopicQuery
from backend.application.get_topic.use_case import GetTopicUseCase
from backend.domain.topic.value_objects import TopicId
from backend.interfaces.http.topics.schemas import (
    GetTopicResponse,
    QuestionResponse,
)

router = APIRouter(prefix='/topics', tags=['topics'])


@router.get('/{topic_id}')
def get_topic(
    topic_id: str,
    uc: Annotated[GetTopicUseCase, Depends(get_get_topic_uc)],
) -> GetTopicResponse:
    query = GetTopicQuery(
        topic_id=TopicId(str(topic_id)),
    )
    try:
        topic = uc.execute(query)
    except TopicNotFound as e:
        return HTTPException(
            status_code=404,
            detail='Topic not found',
        )
    return GetTopicResponse(
        id=topic.id.value,
        version=topic.version.value,
        questions=[QuestionResponse(id=qid.value) for qid in topic.questions],
    )
