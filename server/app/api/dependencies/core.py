from typing import Annotated

from app.utils.database import get_current_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

#DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
DBSessionDep = Annotated[AsyncSession, Depends(get_current_session)]

