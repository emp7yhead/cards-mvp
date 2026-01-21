from http import HTTPStatus


class ApplicationError(Exception): ...

class SessionNotFound(ApplicationError):
    code = "SESSION_NOT_FOUND"
    message = "Session not found"
    http_status = HTTPStatus.NOT_FOUND


class ResultNotFound(ApplicationError):
    code = "RESULT_NOT_FOUND"
    message = "Result not found"
    http_status = HTTPStatus.NOT_FOUND


class InvalidQuestion(ApplicationError):
    code = "INVALID_QUESTION"
    message = "Invalid question"
    http_status = HTTPStatus.BAD_REQUEST


class TopicNotFound(ApplicationError):
    code = "TOPIC_NOT_FOUND"
    message = "Topic not found"
    http_status = HTTPStatus.NOT_FOUND


class ServiceUnavailable(ApplicationError):
    code = "SERVICE_UNAVAILABLE"
    message = "Service unavailable"
    http_status = HTTPStatus.SERVICE_UNAVAILABLE
