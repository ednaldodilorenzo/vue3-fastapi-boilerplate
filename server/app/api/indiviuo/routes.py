from fastapi import APIRouter, Depends, status
from jwt import PyJWTError
from typing import List, Union
from app.utils.auth import decode_jwt
from app.utils.routes import PaginatedParams
from app.utils.exception import CredentialsException
from app.api.dependencies.auth import validate_is_authenticated, PermissionChecker, Roles
from app.api.dependencies.user import CurrentUserDep
from app.api.generic.schemas import PaginatedResponse
from app.utils.objects import create_object_from_instance
from app.models import Individuo
from .service import IIndividuoService, IndividuoService
from .schemas import IndividuoSchema


router = APIRouter(
    prefix="/api/v1/individuo",
    tags=["individuo"],
)


@router.get(
    "",
    dependencies=[Depends(validate_is_authenticated)],
    response_model=Union[PaginatedResponse[IndividuoSchema], List[IndividuoSchema]],
)
async def buscar_todos_por_paroquia(
    current_user: CurrentUserDep,
    q: PaginatedParams = Depends(),
    individuo_service: IIndividuoService = Depends(IndividuoService),
):
    return await individuo_service.buscar_por_paroquia(
        id_paroquia=current_user.id_paroquia, page=q.page, page_size=q.page_size, _filter=q.search, paginate=q.paginate
    )


@router.get("/{_id}", dependencies=[Depends(validate_is_authenticated)])
async def buscar_por_id(
    _id: int,
    individuo_service: IIndividuoService = Depends(IndividuoService),
):
    return await individuo_service.buscar_por_id(_id)


@router.post(
    "",
    dependencies=[Depends(validate_is_authenticated), Depends(PermissionChecker([Roles.ROLE_GESTOR]))],
    status_code=status.HTTP_201_CREATED,
)
async def criar(
    current_user: CurrentUserDep,
    individuo_schema: IndividuoSchema,
    individuo_service: IIndividuoService = Depends(IndividuoService),
):
    individuo = create_object_from_instance(individuo_schema, Individuo)
    individuo.id_paroquia = current_user.id_paroquia
    return await individuo_service.criar(individuo)


@router.get("/token/{token}")
async def buscar_individuo_por_token(token: str, individuo_service: IIndividuoService = Depends(IndividuoService)):
    try:
        payload = decode_jwt(token)
        id_pessoa = payload.get("id_individuo")
        email = payload.get("email")
        pessoa = {}
        if id_pessoa:
            pessoa = await individuo_service.buscar_por_id(id_pessoa)
        else:
            pessoa = {"email": email}
        return pessoa
    except PyJWTError as pje:
        raise CredentialsException("Falha ao decodificar token") from pje


@router.patch("/{_id}", dependencies=[Depends(validate_is_authenticated)])
async def atualizar_individuo(
    _id: int,
    current_user: CurrentUserDep,
    individuo: IndividuoSchema,
    individuo_service: IIndividuoService = Depends(IndividuoService),
):
    """Atualiza os dados do indivíduo. No futuro deverá ser permitido apenas para o próprio indivíduo se for o usuário e o gestor da paróquia.

    Args:
        _id (int): _description_
        individuo (IndividuoSchema): _description_
        individuo_service (_type_, optional): _description_. Defaults to Depends(IndividuoService).

    Returns:
        _type_: _description_
    """
    if current_user.id_individuo != _id and current_user.papel != Roles.ROLE_GESTOR:
        raise CredentialsException("O usuário pode alterar apenas seus dados.")

    return await individuo_service.editar(_id, individuo)


@router.get("/logged/dados")
async def buscar_dados_individuo_logado(
    current_user: CurrentUserDep, individuo_service: IIndividuoService = Depends(IndividuoService)
):
    """Responsável por buscar dados do indivíduo associado ao usuário logado. Serve para permitir que o usuário altere seus próprios dados.

    Args:
        current_user (CurrentUserDep): Usuário logado na aplicação.
        individuo_service (_type_, optional): Arquivo de serviço para o indivíduo. Defaults to Depends(IndividuoService).

    Returns:
        _type_: _description_
    """
    id_pessoa = current_user.id_individuo
    if not id_pessoa:
        return None

    individuo = await individuo_service.buscar_por_id(id_pessoa)

    return individuo
