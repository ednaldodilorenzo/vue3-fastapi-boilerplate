from abc import ABC, abstractmethod
from app.models.usuario import Usuario
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.api.generic.dao import IBaseDao, BaseDao
from app.api.dependencies.core import DBSessionDep


class IUsuarioDao(IBaseDao):

    @abstractmethod
    async def buscar_pelo_login(self, login: str) -> Usuario:
        pass

    @abstractmethod
    async def buscar_logado_por_id(self, _id: int) -> Usuario:
        pass

    @abstractmethod
    async def buscar_admin_pelo_login(self, login: str) -> Usuario:
        pass


class UsuarioDao(BaseDao, IUsuarioDao):

    def __init__(self, db_session: DBSessionDep):
        super().__init__(Usuario, db_session=db_session)

    async def buscar_pelo_login(self, login: str) -> Usuario:
        return (
            await self.db_session.scalars(
                select(Usuario).options(joinedload(Usuario.individuo)).where(Usuario.username == login)
            )
        ).first()

    async def buscar_logado_por_id(self, _id: int) -> Usuario:
        async with self.db_session as session:
            return (await session.scalars(select(Usuario).where(Usuario.id == _id))).first()

    async def buscar_admin_pelo_login(self, login: str) -> Usuario:
        return (
            await self.db_session.scalars(select(Usuario).where(Usuario.username == login, Usuario.papel == "ADMIN"))
        ).first()
