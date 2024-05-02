from fastapi import (FastAPI)
from app.routes import (
    subscriptions,
    auth
)
from starlette.requests import Request
from starlette.responses import Response
from traceback import print_exception
import traceback


from app.const import (
    OPEN_API_DESCRIPTION,
    OPEN_API_TITLE,
)

from app.version import __version__


app = FastAPI(
    title=OPEN_API_TITLE,
    description=OPEN_API_DESCRIPTION,
    version=__version__,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.include_router(subscriptions.router)
app.include_router(auth.router)

@app.get("/")
async def home():
    return {"hello world"}

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # you probably want some kind of logging here
        s = traceback.format_exc()
        print(s)
        # print_exception(e)
        return Response("Internal server error", status_code=500)

app.middleware('http')(catch_exceptions_middleware)