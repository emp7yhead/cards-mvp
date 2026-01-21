from http import HTTPStatus

from backend.domain.errors import DomainError


class SessionError(DomainError): ...

class SessionCompleted(SessionError):
    code = "SESSION_COMPLETED"
    message = "Session already completed"
    http_status = HTTPStatus.CONFLICT


class SessionExpired(SessionError):
    code = "SESSION_EXPIRED"
    message = "Session expired"
    http_status = HTTPStatus.GONE


class UnknownParticipant(SessionError):
    code = "UNKNOWN_PARTICIPANT"
    message = "Unknown participant"
    http_status = HTTPStatus.NOT_FOUND


class TooManyParticipants(SessionError):
    code = "TOO_MANY_PARTICIPANTS"
    message = "Participants limit exceeded"
    http_status = HTTPStatus.NOT_FOUND


class ParticipantAlreadyAnswered(SessionError):
    code = "PARTICIPANT_ALREADY_ANSWERED"
    message = "Participant alredy answered"
    http_status = HTTPStatus.CONFLICT
