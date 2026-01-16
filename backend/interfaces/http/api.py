from fastapi.applications import FastAPI

from backend.interfaces.http.sessions import sessions
from backend.interfaces.http.topics import topics


def setup_routers(app: FastAPI):
    app.include_router(topics.router)
    app.include_router(sessions.router)

