import asyncio
import os
import pytest
import logging
from datetime import date
from contextlib import ExitStack
from sqlalchemy.pool import NullPool
from asyncpg import Connection
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from app import init_app
from app.config import settings
from app.database import Base, get_db_session, sessionmanager
from app.models import Usuario, Paroquia, Individuo, TipoPessoa, Servico, Casal
from app.utils.auth import hash_password
from app.api.dependencies.auth import Roles
from fastapi.testclient import TestClient
import functools

DATABASE_FILE = settings.database_url[settings.database_url.index("///") + 3 :]
logger = logging.getLogger(name=__file__)


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield init_app(start_db=False)


@pytest.fixture
def client(app):

    with TestClient(app) as c:
        yield c


# @pytest.fixture(scope="module")
# def client_with_admin_token():
#     client = TestClient(app)

#     # Create a token for a valid user
#     token = create_access_token(data={"sub": "user1"})

#     # Include the Authorization header with the token in the client
#     client.headers.update({"Authorization": f"Bearer {token}"})

#     yield client


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def run_migrations(connection: Connection):
    config = Config("app/alembic.ini")
    # config.set_main_option("script_location", "app/alembic")
    config.set_main_option("sqlalchemy.url", settings.database_url)
    script = ScriptDirectory.from_config(config)

    def upgrade(rev, context):
        return script._upgrade_revs("head", rev)

    context = MigrationContext.configure(connection, opts={"target_metadata": Base.metadata, "fn": upgrade})

    with context.begin_transaction():
        with Operations.context(context):
            context.run_migrations()


@pytest.fixture(scope="session", autouse=True)
async def connection_test(event_loop):
    sessionmanager.init(settings.database_url, {"poolclass": NullPool})
    yield
    await sessionmanager.close()
    # Remove the test database after tests
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)


@pytest.fixture(scope="function", autouse=True)
async def setup_database(connection_test):
    # Run alembic migrations on test DB
    async with sessionmanager.connect() as connection:
        await connection.run_sync(run_migrations)

    yield


# Each test function is a clean slate
@pytest.fixture(scope="session", autouse=True)
async def transactional_session():
    async with sessionmanager.session() as session:
        try:
            await session.begin()
            yield session
        finally:
            await session.rollback()  # Rolls back the outer transaction


@pytest.fixture(scope="function")
async def db_session(transactional_session):
    yield transactional_session


@pytest.fixture(scope="function")
async def user_factory(db_session):
    async def _user_factory(username, senha, nome, papel, ativo=True, id_individuo=None):
        user = Usuario(username=username, senha=senha, nome=nome, papel=papel, ativo=ativo, id_individuo=id_individuo)
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        db_session.expunge(user)  # removes from the session
        return user

    return _user_factory


@pytest.fixture(scope="function")
async def admin_user(db_session, user_factory):
    password = "123"
    usuario = await user_factory(
        username="admin@test.com",
        senha=hash_password(password),
        nome="Admin Test",
        papel=Roles.ROLE_ADMIN,
    )
    usuario.senha = password
    yield usuario
    await db_session.delete(usuario)
    await db_session.commit()


@pytest.fixture(scope="function")
async def manager_user(db_session, user_factory):
    password = "123"
    usuario = await user_factory(
        username="manager@test.com",
        senha=hash_password(password),
        nome="Manager Test",
        papel=Roles.ROLE_GESTOR,
    )
    usuario.senha = password
    yield usuario
    await db_session.delete(usuario)
    await db_session.commit()


@pytest.fixture(scope="function")
async def dirigente_user(db_session, user_factory):
    password = "123"
    usuario = await user_factory(
        username="dirigente@test.com",
        senha=hash_password(password),
        nome="Dirigente Test",
        papel=Roles.ROLE_DIRIGENTE,
    )
    usuario.senha = password
    yield usuario
    await db_session.delete(usuario)
    await db_session.commit()


@pytest.fixture(scope="function")
async def inactive_user(db_session, user_factory):
    password = "123"
    usuario = await user_factory(
        username="dirigente@test.com",
        senha=hash_password(password),
        nome="Dirigente Test",
        papel=Roles.ROLE_DIRIGENTE,
        ativo=False,
    )
    usuario.senha = password
    yield usuario
    await db_session.delete(usuario)
    await db_session.commit()


@pytest.fixture(scope="function")
async def individuo_factory(db_session):
    async def _individuo_factory(nome, email, telefone, nascimento, apelido, cpf, tipo_pessoa, id_paroquia):
        individuo = Individuo(
            nome=nome,
            email=email,
            telefone=telefone,
            nascimento=nascimento,
            apelido=apelido,
            cpf=cpf,
            tipo_pessoa=tipo_pessoa,
            id_paroquia=id_paroquia,
        )
        db_session.add(individuo)
        await db_session.commit()
        await db_session.refresh(individuo)
        # db_session.expunge(individuo)  # removes from the session
        return individuo

    return _individuo_factory


@pytest.fixture(scope="function")
async def custom_individuo(db_session, individuo_factory, custom_parish):
    individuo = await individuo_factory(
        nome="Test",
        email="individuo@test.com",
        telefone="33445555",
        nascimento=date.today(),
        apelido="Test",
        cpf="23344455511",
        tipo_pessoa=TipoPessoa.solteiro,
        id_paroquia=custom_parish.id,
    )
    yield individuo
    await db_session.delete(individuo)
    await db_session.commit()


@pytest.fixture(scope="function")
async def user_with_person(db_session, user_factory, custom_individuo):
    password = "123"
    usuario = await user_factory(
        username=custom_individuo.email,
        senha=hash_password(password),
        nome=custom_individuo.nome,
        papel=Roles.ROLE_DIRIGENTE,
        id_individuo=custom_individuo.id,
    )
    usuario.senha = password
    yield usuario
    await db_session.delete(usuario)
    await db_session.commit()


@pytest.fixture(scope="function")
async def manager_with_person(db_session, user_factory, custom_individuo):
    password = "123"
    usuario = await user_factory(
        username=custom_individuo.email,
        senha=hash_password(password),
        nome=custom_individuo.nome,
        papel=Roles.ROLE_GESTOR,
        id_individuo=custom_individuo.id,
    )
    usuario.senha = password
    yield usuario
    await db_session.delete(usuario)
    await db_session.commit()


@pytest.fixture(scope="function")
async def parish_factory(db_session):
    @functools.lru_cache(None)
    async def _custom_parish(nome):
        parish = Paroquia(nome=nome)
        db_session.add(parish)
        await db_session.commit()
        await db_session.refresh(parish)
        db_session.expunge(parish)
        return parish

    return _custom_parish


@pytest.fixture(scope="function")
async def custom_parish(db_session, parish_factory):
    parish = await parish_factory("Teste")
    yield parish
    await db_session.delete(parish)
    await db_session.commit()


@pytest.fixture(scope="function")
async def service_factory(db_session):

    async def _service_factory(nome, id_paroquia):
        servico = Servico(nome=nome, id_paroquia=id_paroquia)
        db_session.add(servico)
        await db_session.commit()
        await db_session.refresh(servico)
        db_session.expunge(servico)
        return servico

    return _service_factory


@pytest.fixture(scope="function")
async def custom_service(db_session, service_factory, custom_parish):
    parish = await service_factory("Teste", custom_parish.id)
    yield parish
    await db_session.delete(parish)
    await db_session.commit()


@pytest.fixture(scope="function")
async def couple_factory(db_session):

    async def _couple_factory(id_paroquia):
        esposo = Individuo(
            nome="Teste 1",
            email="test@teswt.com",
            telefone="1234",
            nascimento=date.today(),
            apelido="test",
            cpf="04225633321",
            tipo_pessoa=TipoPessoa.solteiro,
            id_paroquia=id_paroquia,
        )
        esposa = Individuo(
            nome="Teste 2",
            email="test@test.com",
            telefone="12345",
            nascimento=date.today(),
            apelido="test1",
            cpf="04225633312",
            tipo_pessoa=TipoPessoa.solteiro,
            id_paroquia=id_paroquia,
        )
        casal = Casal(
            nome=f"{esposo.nome}/{esposa.nome}",
            esposa=esposa,
            esposo=esposo,
            id_paroquia=id_paroquia,
            observacoes="N/A",
        )
        db_session.add(casal)
        await db_session.commit()
        await db_session.refresh(casal)
        db_session.expunge(casal)
        return casal

    return _couple_factory


@pytest.fixture(scope="function")
async def custom_couple(db_session, couple_factory, custom_parish):
    couple = await couple_factory(custom_parish.id)
    yield couple
    await db_session.delete(couple)
    await db_session.commit()


@pytest.fixture(scope="function")
async def custom_service(db_session, service_factory, custom_parish):
    parish = await service_factory("Teste", custom_parish.id)
    yield parish
    await db_session.delete(parish)
    await db_session.commit()


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, db_session):
    async def get_db_session_override():
        yield db_session[0]

    app.dependency_overrides[get_db_session] = get_db_session_override
