import pytest
from fastapi import status
from app.utils.auth import encode_jwt
from app.api.dependencies.auth import Roles


@pytest.mark.asyncio
async def test_signup(client, custom_parish):
    payload = {"papel": Roles.ROLE_GESTOR, "id_paroquia": custom_parish.id, "email": "test@test.com"}
    jwt = encode_jwt(payload=payload)
    response = client.post(
        f"/api/auth/v1/signup/{jwt}",
        json={
            "email": "test@test.com",
            "nome": "Testing Application",
            "nascimento": "2000-06-18",
            "cpf": "123456789",
            "telefone": "8399988877",
            "senha": "123",
            "confirmacao": "123",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "ok"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    [
        {
            "email": "test",
            "nome": "Testing Application",
            "nascimento": "2000-06-18",
            "cpf": "123456789",
            "telefone": "8399988877",
            "senha": "123",
            "confirmacao": "123",
        },
        {
            "nome": "Testing Application",
            "nascimento": "2000-06-18",
            "cpf": "123456789",
            "telefone": "8399988877",
            "senha": "123",
            "confirmacao": "123",
        },
        {
            "email": "test",
            "nascimento": "2000-06-18",
            "cpf": "123456789",
            "telefone": "8399988877",
            "senha": "123",
            "confirmacao": "123",
        },
        {
            "email": "test",
            "nome": "Testing Application",
            "cpf": "123456789",
            "telefone": "8399988877",
            "senha": "123",
            "confirmacao": "123",
        },
        {
            "email": "test",
            "nome": "Testing Application",
            "nascimento": "2000-06-18",
            "telefone": "8399988877",
            "senha": "123",
            "confirmacao": "123",
        },
        {
            "email": "test",
            "nome": "Testing Application",
            "nascimento": "2000-06-18",
            "cpf": "123456789",
            "senha": "123",
            "confirmacao": "123",
        },
        {
            "email": "test",
            "nome": "Testing Application",
            "nascimento": "2000-06-18",
            "cpf": "123456789",
            "telefone": "8399988877",
            "confirmacao": "123",
        },
        {
            "email": "test",
            "nome": "Testing Application",
            "nascimento": "2000-06-18",
            "cpf": "123456789",
            "telefone": "8399988877",
            "senha": "123",
        },
    ],
)
async def test_signup_bad_request(client, custom_parish, body):
    payload = {"papel": Roles.ROLE_GESTOR, "id_paroquia": custom_parish.id, "email": "test"}
    jwt = encode_jwt(payload=payload)
    response = client.post(
        f"/api/auth/v1/signup/{jwt}",
        json=body,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_signup_email_already_registered(client):
    jwt = "sjfklsjklfjslkdj"
    response = client.post(
        f"/api/auth/v1/signup/{jwt}",
        json={
            "email": "test@test.com",
            "nome": "Testing Application",
            "nascimento": "2000-06-18",
            "cpf": "123456789",
            "telefone": "8399988877",
            "senha": "123",
            "confirmacao": "123",
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_signup_invalid_token(client):
    jwt = "sjfklsjklfjslkdj"
    response = client.post(
        f"/api/auth/v1/signup/{jwt}",
        json={
            "email": "test2@test.com",
            "nome": "Testing Application",
            "nascimento": "2000-06-18",
            "cpf": "123456789",
            "telefone": "8399988877",
            "senha": "123",
            "confirmacao": "123",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
