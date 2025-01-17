from pydantic_core.core_schema import FieldValidationInfo
from pydantic import BaseModel, field_validator


class MudarSenhaSchema(BaseModel):
    senha: str
    nova_senha: str
    confirmacao: str

    @field_validator("confirmacao")
    def passwords_match(cls, v, info: FieldValidationInfo):
        if "nova_senha" in info.data and v != info.data["nova_senha"]:
            raise ValueError("passwords do not match")
        return v


class UsuarioResponse(BaseModel):
    id: int
    username: str
    nome: str
    papel: str
