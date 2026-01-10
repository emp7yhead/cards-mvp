from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from backend.interfaces.http.sessions import sessions

app = FastAPI(default_response_class=ORJSONResponse)

app.include_router(router=sessions.router)
