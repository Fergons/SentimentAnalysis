import asyncio
from typing import AsyncGenerator

import pytest
from fastapi_users.password import get_password_hash
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import config
from app.main import app
from app.models import Base
from app.db.session import async_engine, async_session
from app.tests import utils
from app.api.deps import get_session
from .utils import seed_initial_test_data, is_test_data_seeded

default_user_email = "geralt@wiedzmin.pl"
default_user_hash = get_password_hash("geralt")
superuser_user_email = "yennefer@wiedzmin.pl"
superuser_user_hash = get_password_hash("yennefer")


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client(session) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_session] = lambda: session
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        yield client


@pytest.fixture
async def clear_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def test_db_setup_sessionmaker():
    # assert if we use TEST_DB URL for 100%
    assert config.settings.ENVIRONMENT == "PYTEST"
    assert str(async_engine.url) == config.settings.TEST_SQLALCHEMY_DATABASE_URI

    # always drop and create test db tables between tests session
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return async_session


@pytest.fixture(scope="session")
async def get_session_maker():
    return async_session


@pytest.fixture
async def session(test_db_setup_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with test_db_setup_sessionmaker() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture
async def default_user(session: AsyncSession):
    return await utils.create_db_user(default_user_email, default_user_hash, session)


@pytest.fixture
async def superuser_user(session: AsyncSession):
    return await utils.create_db_user(
        superuser_user_email, superuser_user_hash, session, is_superuser=True
    )


@pytest.fixture
async def access_token(client: AsyncClient):
    access_token_res = await client.post(
        "/auth/jwt/login",
        data={
            "username": "geralt@wiedzmin.pl",
            "password": "geralt",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert access_token_res.status_code == 200
    token = access_token_res.json()
    access_token = token.get("access_token")
    assert access_token is not None
    return access_token


@pytest.fixture
async def test_data(session: AsyncSession):
    if await is_test_data_seeded(session):
        return
    data = await seed_initial_test_data(session)
    return
