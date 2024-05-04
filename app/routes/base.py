from fastapi import APIRouter
from typing import Callable, List

from fastapi import Body, FastAPI, HTTPException, Request, Response
from fastapi.routing import APIRoute
from fastapi.exceptions import (
    HTTPException,
    RequestValidationError
)

import traceback

from app.backend.config import (config)

class BaseRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super(BaseRouter, self).__init__(*args, **kwargs)
        self.route_class = ErrorLoggingRoute


class ErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)
            except Exception as generic_exc:
                if(config.show_debug_info):
                    return Response(content="blablabla".join(
                        traceback.format_exception(
                            generic_exc, value=generic_exc, tb=generic_exc.__traceback__
                        )
                    )
                    , status_code=504)
                else:
                    return Response("Internal server error", status_code=500)                

        return custom_route_handler