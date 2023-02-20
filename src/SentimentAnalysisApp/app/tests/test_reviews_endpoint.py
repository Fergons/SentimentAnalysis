import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import UserDB
from app import models
import logging
from .utils import seed_initial_test_data

logger = logging.getLogger()


# test reviews api endpoints
@pytest.mark.anyio
async def test_read_reviews_endpoint(session: AsyncSession,
                                     client: AsyncClient,
                                     test_data: None):
    resp = await client.get(
        "/reviews/",
        params={"processed": True}
    )
    assert resp.status_code == 200
    data = resp.json()
    logger.info(data)
    assert all([len(review["aspects"]) > 0 and review["processed_at"] is not None for review in data])
    num_processed_reviews = len(data)

    resp = await client.get(
        "/reviews/",
        params={"processed": False}
    )

    assert resp.status_code == 200
    data = resp.json()
    logger.info(data)
    assert all([review["aspects"] == [] for review in data if review["processed_at"] is None])
    assert num_processed_reviews == len([1 for review in data if review["processed_at"] is not None])


@pytest.mark.anyio
async def test_get_review_by_id_endpoint(client: AsyncClient, test_data: None):
    resp = await client.get(
        "/reviews/777"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == 777


@pytest.mark.anyio
async def test_get_summary_endpoint(client: AsyncClient, test_data: None):
    # test get summary endpoint
    resp = await client.get(
        "/reviews/summary/",
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_reviews"] == 11
