import inspect

from fastapi.exceptions import (
    HTTPException,
    RequestValidationError
)
from loguru import logger
from starlette.requests import Request
from starlette.responses import Response
import traceback
import os
from app.backend.config import config

from typing import Callable, List

from fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.routing import APIRoute

def raise_with_log(status_code: int, detail: str) -> None:
    """Wrapper function for logging and raising exceptions."""

    desc = f"<HTTPException status_code={status_code} detail={detail}>"
    logger.error(f"{desc} | runner={runner_info()}")
    raise HTTPException(status_code, detail)


def runner_info() -> str:
    info = inspect.getframeinfo(inspect.stack()[2][0])
    return f"{info.filename}:{info.function}:{info.lineno}"


async def catch_exceptions_middleware(request: Request, call_next) -> Response:
    try:
        return await call_next(request)
    except Exception as e:
        # you probably want some kind of logging here
        s = traceback.format_exc()
        print(s)
        # print_exception(e)
        if(config.show_debug_info):
            return Response("blablabla"
            #                 .join(
            #     traceback.format_exception(
            #         e, value=e, tb=e.__traceback__
            #     )
            # )
            , status_code=500)
        else:
            return Response("Internal server error", status_code=500)

