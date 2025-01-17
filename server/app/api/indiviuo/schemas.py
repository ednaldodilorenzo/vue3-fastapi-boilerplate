from pydantic import BaseModel, EmailStr
from datetime import date


class IndividuoSchema(BaseModel):
    id: int | None = None
    email: EmailStr
    telefone: str
    nascimento: date
    apelido: str
    cpf: str
    nome: str
