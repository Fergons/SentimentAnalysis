import pytest
from httpx import AsyncClient

from app.schemas import UserDB

# All test coroutines in file will be treated as marked (async allowed).
pytestmark = pytest.mark.anyio

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


async def test_get_games_endpoint(client: AsyncClient, default_user: UserDB, access_token: str):
    # test get games endpoint
    resp = await client.get(
        "/games",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data = resp.json()
