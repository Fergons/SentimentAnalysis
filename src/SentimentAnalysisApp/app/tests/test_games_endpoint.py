import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserDB
from app import models
import logging
from .utils import seed_initial_test_data

# All test coroutines in file will be treated as marked (async allowed).
pytestmark = pytest.mark.anyio
logger = logging.getLogger()


async def test_get_games_endpoint(session: AsyncSession,
                                  client: AsyncClient,
                                  default_user: UserDB,
                                  access_token: str,
                                  test_data: None):
    resp = await client.get(
        "/games/",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data = resp.json()
    logger.info(data)


# test get game by id endpoint
async def test_get_game_by_id_endpoint(client: AsyncClient, access_token: str, test_data: None):
    resp = await client.get(
        "/games/22",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 22


# test create game endpoint
async def test_create_game_endpoint(client: AsyncClient, access_token: str, test_data: None):
    resp = await client.post(
        "/games/",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": "test title"
        }
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "test title"


# test update game endpoint
async def test_update_game_endpoint(client: AsyncClient, access_token: str, test_data: None):
    resp = await client.put(
        "/games/22",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": "test title updated"
        }
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "test title updated"
