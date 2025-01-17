import logging
from typing import Union
from fastapi import APIRouter, Depends, Response, status, BackgroundTasks
from app.config import settings
from app.utils.email import send_email_background
from app.api.dependencies.auth import validate_is_authenticated, PermissionChecker, Roles
from app.api.auth.schema import LoginRequest, LoginResponse, EmailSchema, SignupRequest
from app.api.auth.service import AuthService
from app.utils.auth import encode_jwt


router = APIRouter(prefix="/api/auth/v1", tags=["auth"])

LOGGER = logging.getLogger(name=__file__)


@router.post("/login", response_model=Union[LoginResponse, dict])
async def login(usuario_login: LoginRequest, response: Response, auth_service: AuthService = Depends(AuthService)):
    if not (usuario_logado := await auth_service.valida_usuario(usuario_login.usuario, usuario_login.senha)):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {status.HTTP_401_UNAUTHORIZED: "nome de usuário ou senha incorreta"}
    payload = {"user_id": usuario_logado.id, "papel": usuario_logado.papel}
    jwt = encode_jwt(payload=payload)
    return LoginResponse(
        id_usuario=usuario_logado.id, nome_usuario=usuario_logado.nome, papel=usuario_logado.papel, token=jwt
    )


@router.post("/signup/{token}")
async def signup(token: str, signup_request: SignupRequest, auth_service: AuthService = Depends(AuthService)):
    await auth_service.signup_user(token, signup_request)
    return "ok"


@router.post(
    "/email/{_id}/gestor",
    dependencies=[Depends(validate_is_authenticated), Depends(PermissionChecker([Roles.ROLE_ADMIN]))],
)
async def send_email(email: EmailSchema, _id: int, background_tasks: BackgroundTasks):
    payload = {"id_paroquia": _id, "papel": Roles.ROLE_GESTOR, "email": email.email}
    jwt = encode_jwt(payload=payload)
    email_body = f"""
    <h1>Confirmação de Email</h1>
    <p>Click no link abaixo para prosseguir com o cadastro:</p>
    <a href="{settings.app_url}/signup/{jwt}">Cadastro de Novo Usuário</a>
    """
    await send_email_background(
        background_tasks=background_tasks, subject="Acesso GesPar", email_to=email.email, body=email_body
    )
    return "ok"
