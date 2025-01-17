from typing import Annotated

from fastapi import Depends
from jwt import PyJWTError
from app.models.usuario import Usuario
from app.models.casal import Individuo, TipoPessoa
from app.api.usuario.dao import UsuarioDao
from app.api.indiviuo.service import IndividuoService
from app.utils.auth import verify_password, decode_jwt, oauth2_scheme, hash_password
from app.utils.database import transactional
from app.utils.exception import BusinessException, CredentialsException
from app.utils.objects import create_object_from_instance
from app.schemas.auth import TokenData
from app.api.auth.schema import SignupRequest


class AuthService:
    def __init__(self, usuario_dao=Depends(UsuarioDao), individuo_service=Depends(IndividuoService)):
        self.usuario_dao: UsuarioDao = usuario_dao
        self.individuo_service = individuo_service

    async def valida_usuario(self, login: str, senha: str) -> Usuario:
        usuario_logado = None

        usuario_logado = await self.usuario_dao.buscar_pelo_login(login)

        return (
            usuario_logado
            if usuario_logado and usuario_logado.ativo and verify_password(senha, usuario_logado.senha)
            else None
        )

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]) -> Usuario:
        try:
            payload = decode_jwt(token)
            user_id = payload.get("user_id")
            if user_id is None:
                raise Exception("Erro")

            token_data = TokenData(user_id=user_id, permissions="")
        except PyJWTError:
            raise CredentialsException("Falha ao decodificar token")
        user = await self.usuario_dao.buscar_por_id(
            token_data.user_id
        )  # get_user_by_id(db_session, token_data.user_id)
        if user is None:
            raise CredentialsException("Usuário não encontrado")
        return user

    @transactional
    async def signup_user(self, token: str, user: SignupRequest):
        usuario = await self.usuario_dao.buscar_pelo_login(user.email)
        if usuario:
            raise BusinessException("Email do usuário já cadastrado no sistema")

        try:
            payload = decode_jwt(token)
        except PyJWTError as pje:
            print(pje)
            raise CredentialsException("Falha ao decodificar token")
        papel = payload.get("papel")
        id_paroquia = payload.get("id_paroquia")
        email = payload.get("email")

        individuo = await self.individuo_service.buscar_por_cpf(user.cpf)
        if individuo:
            individuo_atualizado = create_object_from_instance(user, Individuo)
            individuo_atualizado.email = email
            await self.individuo_service.editar(individuo.id, individuo_atualizado)
        else:
            individuo = create_object_from_instance(user, Individuo)
            individuo.tipo_pessoa = TipoPessoa.solteiro.value
            individuo.id_paroquia = id_paroquia
            individuo.apelido = user.nome
            individuo.email = email
            individuo = await self.individuo_service.criar(individuo)

        usuario = Usuario()
        usuario.username = email
        usuario.senha = hash_password(user.senha)
        usuario.nome = user.nome
        usuario.papel = papel
        usuario.ativo = True
        usuario.id_individuo = individuo.id
        await self.usuario_dao.criar(usuario)
