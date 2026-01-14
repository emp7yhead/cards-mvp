from pydantic import BaseModel


class GetTopicRequest(BaseModel):
    topic_id: str


class QuestionResponse(BaseModel):
    id: str


class GetTopicResponse(BaseModel):
    id: str
    version: str
    questions: list[QuestionResponse, ...]
