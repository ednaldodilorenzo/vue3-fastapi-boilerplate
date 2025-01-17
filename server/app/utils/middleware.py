from typing import Callable, Awaitable
import logging
import json
from logging.handlers import RotatingFileHandler

from fastapi import Request, Response, status as HTTPStatus

from .database import set_db_session_context, AsyncScopedSession
from starlette.middleware.base import BaseHTTPMiddleware


class MyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        response = Response("Internal server error", status_code=HTTPStatus.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            set_db_session_context(session_id=hash(request))
            response = await call_next(request)
        finally:
            await AsyncScopedSession.remove()  # this includes closing the session as well
            set_db_session_context(session_id=None)

        return response


class StructuredLogger(logging.Logger):
    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        if extra is None:
            extra = {}
        extra["app_name"] = "GesPar"
        super()._log(
            level,
            json.dumps(msg) if isinstance(msg, dict) else msg,
            args,
            exc_info,
            extra,
            stack_info,
            stacklevel=stacklevel,
        )


handler = RotatingFileHandler("app.log", maxBytes=10000, backupCount=3)
logging.setLoggerClass(StructuredLogger)
logger = logging.getLogger(__name__)
logger.addHandler(handler)


class StructureLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info("req:%s;url:%s", request.method, request.url)
        response = await call_next(request)
        logger.info("res:%s", response.status_code)
        return response
