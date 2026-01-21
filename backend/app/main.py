from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from backend.app.lifespan import lifespan
from backend.app.middlewares import setup_middlewares
from backend.interfaces.http.api import setup_routers
from backend.interfaces.http.exception_handlers import setup_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(
        title='Cards MVP',
        version='0.0.1',
        debug=True,
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )

    setup_routers(app)
    setup_exception_handlers(app)
    setup_middlewares(app)
    return app


if __name__ == '__main__':
    create_app()
