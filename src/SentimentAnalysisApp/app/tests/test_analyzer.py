import pytest
from httpx import AsyncClient

from app.schemas import UserDB

# All test coroutines in file will be treated as marked (async allowed).
pytestmark = pytest.mark.anyio

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


async def test_analyzer_endpoints(client: AsyncClient, default_user: UserDB, access_token: str):
    TEST_TEXT = "Nostalgická hra. Portal jsem hrával už jako malej zmrd na bráchovo pc když byl náhodou dýl ve škole nebo venku. I teď mi nějaký level dělá problém :D nejlíp utracených 0,99€ :DD"

    # test analyzer endpoint
    resp = await client.post(
        "/analyzer/analyze", headers={"Authorization": f"Bearer {access_token}"},
        json={
            "text": TEST_TEXT,
            "language": "czech"
        }
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("text") == TEST_TEXT


