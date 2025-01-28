from abc import abstractmethod
from app.api.generic.dao import BaseDao, IBaseDao
from app.api.dependencies.core import DBSessionDep
from app.models import Individuo
from sqlalchemy import select, func


class IIndividuoDao(IBaseDao):
    pass


class IndividuoDao(BaseDao, IIndividuoDao):
    def __init__(self, db_session: DBSessionDep):
        super().__init__(Individuo, db_session)
