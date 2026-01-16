from backend.app.container import container
from backend.application.create_session.use_case import CreateSessionUseCase
from backend.application.get_result.use_case import GetResultUseCase
from backend.application.get_topic.use_case import GetTopicUseCase
from backend.application.join_session.use_case import JoinSessionUseCase
from backend.application.submit_answers.use_case import SubmitAnswersUseCase


def get_submit_answers_uc() -> SubmitAnswersUseCase:
    return container.submit_answers_uc


def get_answers_uc() -> GetResultUseCase:
    return container.get_answers_uc


def get_create_session_uc() -> CreateSessionUseCase:
    return container.create_session_uc


def get_join_session_uc() -> JoinSessionUseCase:
    return container.join_session_uc


def get_topic_uc() -> GetTopicUseCase:
    return container.get_topic_uc
