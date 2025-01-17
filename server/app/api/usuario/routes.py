from fastapi import APIRouter, Depends
from app.api.dependencies.auth import validate_is_authenticated
from app.api.dependencies.user import CurrentUserDep
from .service import UsuarioService, IUsuarioService
from .schemas import MudarSenhaSchema, UsuarioResponse

router = APIRouter(prefix="/api/v1/usuarios")


@router.get("/current", dependencies=[Depends(validate_is_authenticated)], response_model=UsuarioResponse)
def buscar_logado(current_user: CurrentUserDep):
    return current_user


@router.patch("/change-password", dependencies=[Depends(validate_is_authenticated)], response_model=UsuarioResponse)
async def atualizar_usuario(
    current_user: CurrentUserDep,
    usuario_schema: MudarSenhaSchema,
    usuario_service: IUsuarioService = Depends(UsuarioService),
):
    return await usuario_service.atualizar_senha(current_user.id, usuario_schema)
