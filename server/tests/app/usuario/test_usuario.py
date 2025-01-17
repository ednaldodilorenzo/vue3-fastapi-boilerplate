import pytest
from fastapi import status
from app.utils.auth import encode_jwt

prefix = "/api/v1/usuarios"


@pytest.mark.asyncio
async def test_atualizar_usuario(client, dirigente_user):
    payload = {"user_id": dirigente_user.id, "papel": dirigente_user.papel}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.patch(
        f"{prefix}/change-password", json={"senha": dirigente_user.senha, "nova_senha": "321", "confirmacao": "321"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nome"] == "Dirigente Test"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    [
        {"nova_senha": "321", "confirmacao": "321"},
        {"senha": "321", "confirmacao": "456"},
        {"senha": "321"},
        {"confirmacao": "456"},
        {},
    ],
)
async def test_atualizar_usuario_request_invalido(client, dirigente_user, body):
    payload = {"user_id": dirigente_user.id, "papel": dirigente_user.papel}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.patch(f"{prefix}/change-password", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_atualizar_usuario_senha_atual_errada(client, dirigente_user):
    payload = {"user_id": dirigente_user.id, "papel": dirigente_user.papel}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.patch(
        f"{prefix}/change-password", json={"senha": "XXXXX", "nova_senha": "321", "confirmacao": "321"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
