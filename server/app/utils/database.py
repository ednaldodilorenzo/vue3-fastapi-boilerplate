import logging
from typing import Optional, Callable, Awaitable, Any
from contextvars import ContextVar
import functools

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_scoped_session,
    async_sessionmaker,
    AsyncSession,
)

from app.config import settings

# some hints from: https://github.com/teamhide/fastapi-boilerplate/blob/master/core/db/session.py
# https://dev.to/uponthesky/python-post-reviewhow-to-implement-a-transactional-decorator-in-fastapi-sqlalchemy-ein
db_session_context: ContextVar[Optional[int]] = ContextVar("db_session_context", default=None)
engine = create_async_engine(url=settings.database_url, echo=True)


def get_db_session_context() -> int:
    session_id = db_session_context.get()

    if not session_id:
        raise ValueError("Currently no session is available")

    return session_id


def set_db_session_context(*, session_id: int) -> None:
    db_session_context.set(session_id)


AsyncScopedSession = async_scoped_session(
    session_factory=async_sessionmaker(bind=engine, autoflush=False, autocommit=False),
    scopefunc=get_db_session_context,
)


def get_current_session() -> AsyncSession:
    return AsyncScopedSession()


AsyncCallable = Callable[..., Awaitable]
logger = logging.getLogger(name=__file__)


def transactional(func: AsyncCallable) -> AsyncCallable:
    @functools.wraps(func)
    async def _wrapper(*args, **kwargs) -> Awaitable[Any]:
        try:
            db_session = get_current_session()

            if db_session.in_transaction():
                result = await func(*args, **kwargs)
                return result

            async with db_session.begin():
                # automatically committed / rolled back thanks to the context manager
                return_value = await func(*args, **kwargs)

            if return_value:
                await db_session.refresh(return_value)
            # refreshes only if the method has a return value
            return return_value
        except Exception as error:
            logger.info(f"request hash: {get_db_session_context()}")
            logger.exception(error)
            print(error)
            raise

    return _wrapper
