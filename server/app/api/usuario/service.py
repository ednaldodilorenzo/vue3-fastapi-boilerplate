from abc import abstractmethod
from fastapi import Depends
from app.api.generic.service import BaseService, IBaseService
from app.models import Usuario
from app.utils.auth import hash_password, verify_password
from app.utils.database import transactional
from app.utils.exception import BusinessException
from .dao import UsuarioDao
from .schemas import MudarSenhaSchema


class IUsuarioService(IBaseService):

    @abstractmethod
    async def atualizar_senha(self, _id, usuario) -> Usuario:
        pass


class UsuarioService(IUsuarioService, BaseService):
    def __init__(self, usuario_dao=Depends(UsuarioDao)):
        super().__init__(usuario_dao, Usuario)

    @transactional
    async def atualizar_senha(self, _id: int, usuario: MudarSenhaSchema) -> Usuario:
        usuario_atual = await self.buscar_por_id(_id)
        if not verify_password(usuario.senha, usuario_atual.senha):
            raise BusinessException("Senha atual incorreta!")

        usuario_atual.senha = hash_password(usuario.nova_senha)
        return usuario_atual
