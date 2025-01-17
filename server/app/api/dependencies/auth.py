from app.api.auth.schema import CurrentUserInfo
from fastapi import HTTPException, status

from .user import CurrentUserDep


async def validate_is_authenticated(
    current_user: CurrentUserDep,
) -> CurrentUserInfo:
    """
    This just returns as the CurrentUserDep dependency already throws if there is an issue with the auth token.
    """
    return current_user


class Roles:
    ROLE_ADMIN = "ADMIN"
    ROLE_GESTOR = "GESTOR"
    ROLE_DIRIGENTE = "DIRIGENTE"


class PermissionChecker:
    def __init__(self, required_permissions: list[str]) -> None:
        self.required_permissions = required_permissions

    def __call__(self, current_user: CurrentUserDep) -> bool:
        if not current_user.papel in self.required_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User has not privileges to access resource"
            )

        return True
