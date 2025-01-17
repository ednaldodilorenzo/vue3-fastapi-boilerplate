import pytest
from fastapi import status
from app.api.dependencies.auth import Roles


@pytest.mark.asyncio
async def test_admin_login(client, admin_user):
    response = client.post("/api/auth/v1/login", json={"usuario": admin_user.username, "senha": admin_user.senha})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nome_usuario"] == admin_user.nome
    assert response.json()["papel"] == Roles.ROLE_ADMIN


@pytest.mark.asyncio
async def test_manager_login(client, manager_user):
    response = client.post("/api/auth/v1/login", json={"usuario": manager_user.username, "senha": manager_user.senha})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nome_usuario"] == manager_user.nome
    assert response.json()["papel"] == Roles.ROLE_GESTOR


@pytest.mark.asyncio
async def test_dirigente_login(client, dirigente_user):
    response = client.post(
        "/api/auth/v1/login", json={"usuario": dirigente_user.username, "senha": dirigente_user.senha}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nome_usuario"] == dirigente_user.nome
    assert response.json()["papel"] == Roles.ROLE_DIRIGENTE


@pytest.mark.asyncio
async def test_inactive_login(client, inactive_user):
    response = client.post("/api/auth/v1/login", json={"usuario": inactive_user.username, "senha": inactive_user.senha})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"401": "nome de usuário ou senha incorreta"}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password",
    [
        ("admin@gespar.com", "321"),
        ("test@gespar.com", "123"),
    ],
)
async def test_login_wrong_credentials(client, username, password):
    response = client.post("/api/auth/v1/login", json={"usuario": username, "senha": password})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"401": "nome de usuário ou senha incorreta"}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "result, body",
    [
        ([{"loc": "body", "field": "usuario", "message": "Field required", "type": "missing"}], {"senha": "321"}),
        (
            [{"loc": "body", "field": "senha", "message": "Field required", "type": "missing"}],
            {"usuario": "test@test.com"},
        ),
        (
            [
                {"loc": "body", "field": "usuario", "message": "Field required", "type": "missing"},
                {"loc": "body", "field": "senha", "message": "Field required", "type": "missing"},
            ],
            {},
        ),
        (
            [
                {
                    "loc": "body",
                    "field": "usuario",
                    "message": "value is not a valid email address: The email address is not valid. It must have exactly one @-sign.",
                    "type": "value_error",
                }
            ],
            {"usuario": "admin", "senha": "321"},
        ),
    ],
)
async def test_login_bad_request(client, result, body):
    response = client.post("/api/auth/v1/login", json=body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": result}
