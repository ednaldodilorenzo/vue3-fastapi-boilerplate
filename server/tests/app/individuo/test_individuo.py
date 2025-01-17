import pytest
from fastapi import status
from app.utils.auth import encode_jwt


@pytest.mark.asyncio
async def test_buscar_logado_individuo_nao_associado(client, manager_user):
    payload = {"user_id": manager_user.id, "papel": manager_user.papel}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.get("/api/v1/individuo/logged/dados")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == None


@pytest.mark.asyncio
async def test_buscar_logado_individuo_associado(client, user_with_person):
    payload = {"user_id": user_with_person.id, "papel": user_with_person.papel}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.get("/api/v1/individuo/logged/dados")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nome"] == user_with_person.nome
    assert response.json()["email"] == user_with_person.username


@pytest.mark.asyncio
async def test_buscar_logado_individuo_inexistente(client):
    payload = {"user_id": 25, "papel": "GESTOR"}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.get("/api/v1/individuo/logged/dados")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_buscar_invalid_token(client):
    jwt = "sljfklajskfljsakj"
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.get("/api/v1/individuo/logged/dados")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_criar_individuo_not_allowed(client, user_with_person):
    payload = {"user_id": user_with_person.id, "papel": user_with_person.papel}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.post(
        "/api/v1/individuo",
        json={
            "email": "test@test.com",
            "telefone": "83877788899",
            "nascimento": "2024-08-04",
            "apelido": "Test",
            "cpf": "99999999999",
            "nome": "Testing Create",
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_criar_individuo(client, manager_with_person, custom_parish):
    payload = {"user_id": manager_with_person.id, "papel": manager_with_person.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.post(
        "/api/v1/individuo",
        json={
            "email": "test@test.com",
            "telefone": "83877788899",
            "nascimento": "2024-08-04",
            "apelido": "Test",
            "cpf": "99999999999",
            "nome": "Testing Create",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["id"] is not None
    _id = response.json()["id"]
    response = client.get(f"/api/v1/individuo/{_id}")
    assert response.json()["nome"] == "Testing Create"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    [
        {
            "telefone": "83877788899",
            "nascimento": "2024-08-04",
            "apelido": "Test",
            "cpf": "78945612345",
        },
        {
            "email": "test@test.com",
            "nascimento": "2024-08-04",
            "apelido": "Test",
            "cpf": "78945612345",
        },
        {
            "email": "test@test.com",
            "telefone": "83877788899",
            "apelido": "Test",
            "cpf": "78945612345",
        },
        {
            "email": "test@test.com",
            "telefone": "83877788899",
            "nascimento": "2024-08-04",
            "cpf": "78945612345",
        },
        {
            "email": "test@test.com",
            "telefone": "83877788899",
            "nascimento": "2024-08-04",
            "apelido": "Test",
        },
    ],
)
async def test_criar_individuo_missing_fields(client, manager_with_person, body):
    payload = {"user_id": manager_with_person.id, "papel": manager_with_person.papel}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.post(
        "/api/v1/individuo",
        json=body,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_atualizar_individuo(client, user_with_person):
    payload = {"user_id": user_with_person.id, "papel": user_with_person.papel}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.patch(
        f"/api/v1/individuo/{user_with_person.id_individuo}",
        json={
            "email": "test@test.com",
            "telefone": "83877788899",
            "nascimento": "2024-08-04",
            "apelido": "Test",
            "cpf": "78945612345",
            "nome": "Testing App",
        },
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    [
        {
            "telefone": "83877788899",
            "nascimento": "2024-08-04",
            "apelido": "Test",
            "cpf": "78945612345",
        },
        {
            "email": "test@test.com",
            "nascimento": "2024-08-04",
            "apelido": "Test",
            "cpf": "78945612345",
        },
        {
            "email": "test@test.com",
            "telefone": "83877788899",
            "apelido": "Test",
            "cpf": "78945612345",
        },
        {
            "email": "test@test.com",
            "telefone": "83877788899",
            "nascimento": "2024-08-04",
            "cpf": "78945612345",
        },
        {
            "email": "test@test.com",
            "telefone": "83877788899",
            "nascimento": "2024-08-04",
            "apelido": "Test",
        },
    ],
)
async def test_atualizar_individuo_missing_fields(client, user_with_person, body):
    payload = {"user_id": user_with_person.id, "papel": user_with_person.papel}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.patch(
        f"/api/v1/individuo/{user_with_person.id_individuo}",
        json=body,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
