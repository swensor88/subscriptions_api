from fastapi import (FastAPI)
from app.routes import (
    subscriptions,
    auth
)
from traceback import print_exception
from app.exc import (
    catch_exceptions_middleware
)
import traceback


from app.const import (
    OPEN_API_DESCRIPTION,
    OPEN_API_TITLE,
)

from app.version import __version__
from fastapi.responses import RedirectResponse


app = FastAPI(
    title=OPEN_API_TITLE,
    description=OPEN_API_DESCRIPTION,
    version=__version__,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)
# app.middleware('http')(catch_exceptions_middleware)


@app.get("/", response_class=RedirectResponse)
async def send_to_swagger():
    return "/docs"

app.include_router(subscriptions.router)
app.include_router(auth.router)

