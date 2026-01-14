from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from backend.app.container import prewarm_topic_uc
from backend.interfaces.http.sessions import sessions
from backend.interfaces.http.topics import topics

app = FastAPI(default_response_class=ORJSONResponse)


@app.on_event("startup")
async def prewarm_topics():
    prewarm_topic_uc.execute()

app.include_router(router=sessions.router)
app.include_router(router=topics.router)
