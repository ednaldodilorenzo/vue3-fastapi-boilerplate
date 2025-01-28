from typing import Annotated

from app.api.auth.schema import CurrentUserInfo
from app.api.usuario.dao import UsuarioDao
from app.schemas.auth import TokenData
from app.utils.auth import decode_jwt, oauth2_scheme
from fastapi import Depends, HTTPException, status
from jwt import PyJWTError


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], usuario_dao=Depends(UsuarioDao)
) -> CurrentUserInfo:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_jwt(token)
        user_id = payload.get("user_id")
        id_paroquia = payload.get("id_paroquia")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, permissions="")
    except PyJWTError:
        raise credentials_exception
    user = await usuario_dao.buscar_logado_por_id(token_data.user_id)
    if user is None:
        raise credentials_exception
    return CurrentUserInfo(
        id=user.id,
        nome=user.nome,
        username=user.username,
        papel=user.papel,
    )


CurrentUserDep = Annotated[CurrentUserInfo, Depends(get_current_user)]
