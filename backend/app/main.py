from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from backend.app.lifespan import lifespan
from backend.interfaces.http.api import setup_routers


def create_app() -> FastAPI:
    app = FastAPI(
        title='Cards MVP',
        version='0.0.1',
        debug=True,
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
    )

    setup_routers(app)
    return app


if __name__ == '__main__':
    create_app()
