from pydantic import BaseModel, ConfigDict
from typing import Optional


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    slug: str
    email: str
    first_name: str
    last_name: str
    is_superuser: bool = False


class UsuarioLogin(BaseModel):
    usuario: str
    senha: str
    paroquia: Optional[int] = None


class UserPrivate(User):
    hashed_password: str
