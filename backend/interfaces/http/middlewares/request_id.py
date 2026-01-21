import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from backend.app.logging.context import request_id_ctx


class RequestIdMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get('X-Request-Id')
        if not request_id:
            request_id = uuid.uuid4().hex

        token = request_id_ctx.set(request_id)

        try:
            response: Response = await call_next(request)
            response.headers['X-Request-Id'] = request_id
            return response
        finally:
            request_id_ctx.reset(token)
