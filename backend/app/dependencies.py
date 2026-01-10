from backend.app.container import get_answers_uc, submit_answers_uc
from backend.application.get_result.use_case import GetResultUseCase
from backend.application.submit_answers.use_case import SubmitAnswersUseCase


def get_submit_answers_uc() -> SubmitAnswersUseCase:
    return submit_answers_uc


def get_get_answers_uc() -> GetResultUseCase:
    return get_answers_uc
