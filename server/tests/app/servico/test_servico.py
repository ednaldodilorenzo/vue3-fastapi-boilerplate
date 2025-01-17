import pytest
from fastapi import status
from app.utils.auth import encode_jwt

PREFIX = "/api/v1/servicos"


@pytest.mark.asyncio
async def test_buscar_servicos(client, manager_user, custom_parish):
    payload = {"user_id": manager_user.id, "papel": manager_user.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.get(PREFIX)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_buscar_servicos_user_not_allowed(client, dirigente_user):
    payload = {"user_id": dirigente_user.id, "papel": dirigente_user.papel}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.get(PREFIX)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_criar_servico(client, manager_user, custom_parish):
    payload = {"user_id": manager_user.id, "papel": manager_user.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.post(PREFIX, json={"nome": "Testing"})
    assert response.status_code == status.HTTP_200_OK
    _id = response.json()["id"]
    assert id is not None
    response = client.get(f"{PREFIX}/{_id}")
    assert response.json()["nome"] == "Testing"


@pytest.mark.asyncio
async def test_criar_servico_mandatory_field(client, manager_user, custom_parish):
    payload = {"user_id": manager_user.id, "papel": manager_user.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.post(PREFIX, json={})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_criar_servico_not_allowed(client, admin_user, custom_parish):
    payload = {"user_id": admin_user.id, "papel": admin_user.papel, "id_paroquia": custom_parish.id}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.post(PREFIX, json={"nome": "Testing"})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_atualizar_servico(client, manager_user, custom_service):
    payload = {"user_id": manager_user.id, "papel": manager_user.papel, "id_paroquia": custom_service.id_paroquia}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.patch(f"{PREFIX}/{custom_service.id}", json={"nome": "New Testing"})
    assert response.status_code == status.HTTP_200_OK
    _id = response.json()["id"]
    assert id is not None
    response = client.get(f"{PREFIX}/{_id}")
    assert response.json()["nome"] == "New Testing"


@pytest.mark.asyncio
async def test_atualizar_servico_bad_request(client, manager_user, custom_service):
    payload = {"user_id": manager_user.id, "papel": manager_user.papel, "id_paroquia": custom_service.id_paroquia}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.patch(f"{PREFIX}/{custom_service.id}", json={})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_atualizar_servico_forbidden(client, admin_user, custom_service):
    payload = {"user_id": admin_user.id, "papel": admin_user.papel, "id_paroquia": custom_service.id_paroquia}
    jwt = encode_jwt(payload=payload)
    client.headers.update({"Authorization": f"Bearer {jwt}"})
    response = client.patch(f"{PREFIX}/{custom_service.id}", json={"nome": "New Testing"})
    assert response.status_code == status.HTTP_403_FORBIDDEN
