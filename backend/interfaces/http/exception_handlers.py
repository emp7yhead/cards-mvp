import logging

from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from backend.application.errors import ApplicationError
from backend.domain.errors import DomainError

logger = logging.getLogger(__name__)


def application_error_handler(
    request: Request,
    exc: ApplicationError,
) -> ORJSONResponse:
    return ORJSONResponse(
        status_code=exc.http_status,
        content={
            'error': {
                'code': exc.code,
                'message': exc.message,
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
            'error': {
                'code': exc.code,
                'message': exc.message,
            },
        },
    )


async def unhandled_exception_handler(request, exc):
    logger.exception(
        'Unhandled exception',
        extra={'path': request.url.path},
    )
    return ORJSONResponse(status_code=500)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.add_exception_handler(ApplicationError, application_error_handler)
    app.add_exception_handler(DomainError, domain_error_handler)

