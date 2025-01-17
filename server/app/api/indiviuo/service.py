from fastapi import Depends
from app.api.generic.service import BaseService, IBaseService
from app.models import Individuo
from .dao import IndividuoDao, IIndividuoDao
from abc import abstractmethod


class IIndividuoService(IBaseService):

    @abstractmethod
    async def buscar_por_cpf(self, cpf: str) -> Individuo:
        pass

    @abstractmethod
    async def buscar_por_paroquia(
        self, id_paroquia: int, page: int, page_size: int, _filter: str, paginate: bool = True
    ) -> list[Individuo]:
        pass


class IndividuoService(IIndividuoService, BaseService):
    def __init__(self, individuo_dao: IIndividuoDao = Depends(IndividuoDao)):
        super().__init__(individuo_dao, Individuo)

    async def buscar_por_cpf(self, cpf: str) -> Individuo:
        return await self._dao.buscar_por_cpf(cpf)

    async def buscar_por_paroquia(
        self, id_paroquia: int, page: int, page_size: int, _filter: str, paginate: bool = True
    ) -> list[Individuo]:
        return await self._dao.buscar_por_paroquia(id_paroquia, page, page_size, _filter, paginate)
