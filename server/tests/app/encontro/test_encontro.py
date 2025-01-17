import pytest
from fastapi import status
from app.utils.auth import encode_jwt

PREFIX = "/api/v1/encontros"


@pytest.mark.asyncio
async def test_buscar_encontros(client, manager_user, custom_parish, custom_service):
    payload = {"user_id": manager_user.id, "papel": manager_user.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.get(f"{PREFIX}?servico={custom_service.id}")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_buscar_encontros_user_not_allowed(client, dirigente_user):
    payload = {"user_id": dirigente_user.id, "papel": dirigente_user.papel}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.get(PREFIX)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_criar_encontro(client, manager_user, custom_parish, custom_service):
    payload = {"user_id": manager_user.id, "papel": manager_user.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.post(
        PREFIX,
        json={
            "nome": "Testing",
            "tema": "Test",
            "ano": "2023",
            "data_inicio": "2024-05-01",
            "data_termino": "2024-05-03",
            "id_servico": custom_service.id,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    _id = response.json()["id"]
    assert _id is not None
    response = client.get(f"{PREFIX}/{_id}")
    assert response.json()["nome"] == "Testing"


@pytest.mark.asyncio
async def test_criar_encontro_not_allowed(client, admin_user, custom_parish, custom_service):
    payload = {"user_id": admin_user.id, "papel": admin_user.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.post(
        PREFIX,
        json={
            "nome": "Testing",
            "tema": "Test",
            "ano": "2023",
            "data_inicio": "2024-05-01",
            "data_termino": "2024-05-03",
            "id_servico": custom_service.id,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_criar_encontro_period_not_valid(client, manager_user, custom_parish, custom_service):
    payload = {"user_id": manager_user.id, "papel": manager_user.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.post(
        PREFIX,
        json={
            "nome": "Testing",
            "tema": "Test",
            "ano": "2023",
            "data_inicio": "2024-05-03",
            "data_termino": "2024-05-01",
            "id_servico": custom_service.id,
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    [
        {
            "tema": "Test",
            "ano": "2023",
            "data_inicio": "2024-05-01",
            "data_termino": "2024-05-03",
        },
        {
            "nome": "Testing",
            "ano": "2023",
            "data_inicio": "2024-05-01",
            "data_termino": "2024-05-03",
        },
        {
            "nome": "Testing",
            "tema": "Test",
            "data_inicio": "2024-05-01",
            "data_termino": "2024-05-03",
        },
        {
            "nome": "Testing",
            "tema": "Test",
            "ano": "2023",
            "data_termino": "2024-05-03",
        },
        {
            "nome": "Testing",
            "tema": "Test",
            "ano": "2023",
            "data_inicio": "2024-05-03",
        },
    ],
)
async def test_criar_encontro_mandatory_field(client, manager_user, custom_parish, custom_service, body):
    payload = {"user_id": manager_user.id, "papel": manager_user.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    body["id_servico"] = custom_service.id
    response = client.post(
        PREFIX,
        json=body,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
