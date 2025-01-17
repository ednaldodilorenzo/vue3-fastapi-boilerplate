from datetime import date
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    usuario: EmailStr
    senha: str


class LoginResponse(BaseModel):
    id_usuario: int
    nome_usuario: str
    papel: str
    token: str


class EmailSchema(BaseModel):
    email: EmailStr


class SignupRequest(BaseModel):
    email: EmailStr
    nome: str
    nascimento: date
    cpf: str
    telefone: str
    senha: str
    confirmacao: str


class CurrentUserInfo(BaseModel):
    id: int
    nome: str
    username: str
    papel: str
    id_individuo: int | None = None
    id_paroquia: int | None = None
