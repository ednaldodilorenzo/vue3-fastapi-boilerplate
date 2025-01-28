from abc import ABC, abstractmethod
from sqlalchemy import select, func, Select, update
from sqlalchemy.ext.asyncio import AsyncSession


class IBaseDao(ABC):

    @abstractmethod
    async def criar(self, item):
        pass

    @abstractmethod
    async def buscar_todos(self, page: int, page_size: int, pagination: bool = True):
        pass

    @abstractmethod
    async def alterar(self, _id, item):
        pass

    @abstractmethod
    async def buscar_por_id(self, id_entity):
        pass

    @abstractmethod
    async def paginate(self, query: Select, page: int, page_size: int) -> dict:
        pass

    @abstractmethod
    async def delete(self, item):
        pass


class BaseDao:
    def __init__(self, entity, db_session: AsyncSession):
        self.db_session = db_session
        self._entity = entity

    async def criar(self, item):
        self.db_session.add(item)
        await self.db_session.flush()
        return item

    async def alterar(self, _id, item):
        result = await self.db_session.execute(
            update(self._entity)
            .where(self._entity.id == _id)
            .values(item)
            .returning(self._entity)
        )

        return result.scalars().first()

    async def buscar_todos(
        self, page: int, page_size: int, pagination: bool = True, filter: str = ""
    ):
        query = select(self._entity)

        if filter:
            query = query.where(self._entity.filter == filter)

        return (
            await self.paginate(query, page, page_size)
            if pagination
            else (await self.db_session.scalars(query)).all()
        )

    async def buscar_por_id(self, id_entity):
        return (
            await self.db_session.scalars(
                select(self._entity).where(self._entity.id == id_entity)
            )
        ).first()

    async def paginate(self, query: Select, page: int, page_size: int) -> dict:
        return {
            "count": await self.db_session.scalar(
                select(func.count()).select_from(query.subquery())
            ),
            "items": (
                await self.db_session.scalars(
                    query.limit(page_size).offset((page - 1) * page_size)
                )
            ).all(),
            "page": page,
            "page_size": page_size,
        }

    async def delete(self, item):
        return await self.db_session.delete(item)
