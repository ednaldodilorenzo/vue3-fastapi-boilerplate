from abc import abstractmethod
from app.api.generic.dao import BaseDao, IBaseDao
from app.api.dependencies.core import DBSessionDep
from app.models import Individuo
from sqlalchemy import select, func


class IIndividuoDao(IBaseDao):

    @abstractmethod
    async def buscar_por_cpf(self, cpf: str) -> Individuo:
        pass

    @abstractmethod
    async def buscar_por_paroquia(self, id_paroquia: int, page: int, page_size: int, _filter: str) -> Individuo:
        pass


class IndividuoDao(BaseDao, IIndividuoDao):
    def __init__(self, db_session: DBSessionDep):
        super().__init__(Individuo, db_session)

    async def buscar_por_cpf(self, cpf: str) -> Individuo:
        return (await self.db_session.scalars(select(Individuo).where(Individuo.cpf == cpf))).first()

    async def buscar_por_paroquia(
        self, id_paroquia: int, page: int, page_size: int, _filter: str, paginate=True
    ) -> Individuo:
        query = (
            select(Individuo).where(
                Individuo.id_paroquia == id_paroquia, func.lower(Individuo.extenso).like("%{}%".format(_filter.lower()))
            )
            if _filter
            else select(Individuo)
        )
        return await self.paginate(query, page, page_size) if paginate else (await self.db_session.scalars(query)).all()
