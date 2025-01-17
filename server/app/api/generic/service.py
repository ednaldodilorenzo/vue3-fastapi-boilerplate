from app.utils.database import transactional
from abc import abstractmethod, ABC


class IBaseService(ABC):
    @abstractmethod
    async def criar(self, item):
        pass

    @abstractmethod
    async def alterar(self, _id, item):
        pass

    @abstractmethod
    async def editar(self, _id, item):
        pass

    @abstractmethod
    async def buscar_todos(self, page, page_size):
        pass

    @abstractmethod
    async def buscar_por_id(self, _id):
        pass

    @abstractmethod
    async def delete(self, item):
        pass


class BaseService(IBaseService):
    def __init__(self, dao, entity):
        self._dao = dao
        self._entity = entity

    @transactional
    async def criar(self, item):
        return await self._dao.criar(item)

    @transactional
    async def alterar(self, _id, item):
        return await self._dao.alterar(_id, item)

    @transactional
    async def editar(self, _id, item):
        current_item = await self.buscar_por_id(_id)
        if not current_item:
            raise KeyError("Item to update not found")
        for var, value in vars(item).items():
            not var.startswith("_") and value and setattr(current_item, var, value)
        return current_item

    async def buscar_todos(self, page, page_size):
        return await self._dao.buscar_todos(page, page_size)

    async def buscar_por_id(self, _id):
        result = await self._dao.buscar_por_id(_id)

        if not result:
            raise KeyError("Item not found")

        return result

    async def delete(self, item):
        return await self._dao.delete(item)
