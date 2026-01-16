from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from backend.application.errors import ApplicationError
from backend.domain.errors import DomainError


def application_error_handler(
    request: Request,
    exc: ApplicationError,
) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=exc.http_status,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            },
        },
    )


def domain_error_handler(
    request: Request,
    exc: DomainError,
) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=exc.http_status,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            },
        },
    )


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApplicationError, application_error_handler)
    app.add_exception_handler(DomainError, domain_error_handler)

