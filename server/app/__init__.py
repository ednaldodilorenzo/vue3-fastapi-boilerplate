from contextlib import asynccontextmanager
from pydantic import ValidationError
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError
from .database import sessionmanager
from .config import settings
from .version import __version__
from .utils.feature_flags import feature_flags


def init_app(start_db: bool = True) -> FastAPI:
    lifespan = None

    if start_db:
        sessionmanager.init(
            settings.database_url,
            {"echo": settings.echo_sql, "pool_size": settings.pool_size, "pool_timeout": settings.pool_timeout},
        )

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            """
            Function that handles startup and shutdown events.
            To understand more, read https://fastapi.tiangolo.com/advanced/events/
            """
            feature_flags.load_feature_flags()
            yield

            if sessionmanager._engine is not None:
                # Close the DB connection
                await sessionmanager.close()

    server = FastAPI(lifespan=lifespan, title=settings.project_name, docs_url="/api/docs", version=__version__)
    origins = ["*"]
    server.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    server.add_middleware(GZipMiddleware, minimum_size=1000)

    from . import api
    from .utils.exception import BusinessException, CredentialsException
    from .utils.exception_handlers import (
        unhandled_exception_handler,
        validation_exception_handler,
        validation_request_exception_handler,
        validation_business_exception,
        validation_credentials_exception,
    )
    from .utils.middleware import MyMiddleware, StructureLogMiddleware

    # Routers
    server.include_router(api.auth_router)
    server.include_router(api.individuo_router)
    server.include_router(api.usuario_router)
    server.add_exception_handler(RequestValidationError, validation_request_exception_handler)
    server.add_exception_handler(BusinessException, validation_business_exception)
    server.add_exception_handler(ValidationError, validation_exception_handler)
    server.add_exception_handler(CredentialsException, validation_credentials_exception)
    server.add_exception_handler(Exception, unhandled_exception_handler)
    server.add_middleware(MyMiddleware)
    server.add_middleware(StructureLogMiddleware)

    return server
