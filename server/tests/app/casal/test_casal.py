import pytest
from fastapi import status
from app.utils.auth import encode_jwt

PREFIX = "/api/v1/casais"


@pytest.mark.asyncio
async def test_buscar_todos(client, manager_user, custom_parish):
    payload = {"user_id": manager_user.id, "papel": manager_user.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.get(PREFIX)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_buscar_casais_user_not_allowed(client, dirigente_user, custom_parish):
    payload = {"user_id": dirigente_user.id, "papel": dirigente_user.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.get(PREFIX)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_criar_casal_individuos_nao_cadastrados(client, manager_user, custom_parish):
    payload = {"user_id": manager_user.id, "papel": manager_user.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.post(
        PREFIX,
        json={
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    _id = response.json()["id"]
    assert id is not None
    response = client.get(f"{PREFIX}/{_id}")
    assert response.json()["nome"] == "Teste/Testa"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    [
        {
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "observacoes": "Nenhhuma",
        },
    ],
)
async def test_criar_casal_missing_fields(client, manager_with_person, body):
    payload = {"user_id": manager_with_person.id, "papel": manager_with_person.papel}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.post(
        PREFIX,
        json=body,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_criar_casal_not_allowed(client, admin_user, custom_parish):
    payload = {"user_id": admin_user.id, "papel": admin_user.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.post(PREFIX, json={"nome": "Testing"})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_criar_casal_um_individuo_cadastrado(client, manager_user, custom_parish, custom_individuo):
    payload = {"user_id": manager_user.id, "papel": manager_user.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.post(
        PREFIX,
        json={
            "id_esposo": custom_individuo.id,
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    _id = response.json()["id"]
    assert id is not None
    response = client.get(f"{PREFIX}/{_id}")
    assert response.json()["nome"] == "Teste/Testa"


@pytest.mark.asyncio
async def test_alterar_casal(client, manager_user, custom_parish, custom_couple):
    payload = {"user_id": manager_user.id, "papel": manager_user.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.patch(
        f"{PREFIX}/{custom_couple.id}",
        json={
            "id": custom_couple.id,
            "id_esposo": custom_couple.esposo.id,
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "id_esposa": custom_couple.esposa.id,
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    _id = response.json()["id"]
    assert id is not None
    response = client.get(f"{PREFIX}/{_id}")
    assert response.json()["nome"] == "Teste/Testa"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    [
        {
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "apelido_esposa": "Testa",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "cpf_esposa": "789778979",
            "observacoes": "Nenhhuma",
        },
        {
            "nome_esposo": "Testando esposo",
            "email_esposo": "test@test.com",
            "telefone_esposo": "787897897",
            "nascimento_esposo": "1988-05-26",
            "apelido_esposo": "Teste",
            "cpf_esposo": "054887899",
            "nome_esposa": "Testando esposa",
            "email_esposa": "tests@test.com",
            "telefone_esposa": "87897845465",
            "nascimento_esposa": "1988-05-26",
            "apelido_esposa": "Testa",
            "observacoes": "Nenhhuma",
        },
    ],
)
async def test_alterar_casal_missing_fields(client, manager_with_person, custom_parish, body, custom_couple):
    payload = {"user_id": manager_with_person.id, "papel": manager_with_person.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.patch(
        f"{PREFIX}/{custom_couple.id}",
        json=body,
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_alterar_casal_not_allowed(client, admin_user, custom_parish, custom_couple):
    payload = {"user_id": admin_user.id, "papel": admin_user.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.patch(f"{PREFIX}/{custom_couple.id}", json={"nome": "Testing"})
    assert response.status_code == status.HTTP_403_FORBIDDEN
