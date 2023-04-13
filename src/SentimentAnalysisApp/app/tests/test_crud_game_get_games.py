from datetime import datetime, timezone, timedelta
import random

import pytest
import httpx
import respx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlalchemy.orm import selectinload
from app import crud, schemas, models
import asyncio
import logging

from core.cursor import decode_cursor

pytestmark = pytest.mark.anyio

logger = logging.getLogger()


def games_compare_str(games: List[schemas.GameListItem]):
    return "\n".join(
        [f"{g.id:<10} {g.name:<30} {g.release_date.isoformat():<30} {g.score:<10}" for g in games])


async def test_crud_game_get_game_list(session: AsyncSession, test_data: None):
    response = await crud.game.get_game_list(session)
    logger.debug(response)
    logger.debug(f"Games:\n{games_compare_str(response.games)}")
    assert response.query_summary is not None
    assert response.query_summary.total == 4
    assert len(response.games) == response.query_summary.total


async def test_game_list_min_score_filter(session: AsyncSession):
    filter = schemas.GameListFilter(
        min_score=1
    )
    response = await crud.game.get_game_list(session, filter=filter)
    logger.debug([(g.id, g.name, g.score) for g in response.games])
    assert response.query_summary is not None
    assert response.query_summary.total > 0
    assert len(response.games) == response.query_summary.total
    for game in response.games:
        assert float(game.score) >= 1


async def test_game_list_max_score_filter(session: AsyncSession):
    filter = schemas.GameListFilter(
        max_score=5.0
    )
    response = await crud.game.get_game_list(session, filter=filter)
    logger.debug([(g.id, g.name, g.score) for g in response.games])
    assert response.query_summary is not None
    assert response.query_summary.total == 3
    assert len(response.games) == response.query_summary.total

    for game in response.games:
        assert float(game.score) <= 5.0


async def test_game_list_sort_by_score_asc(session: AsyncSession):
    sort = schemas.GameListSort(
        score="asc"
    )
    response = await crud.game.get_game_list(session, sort=sort)
    logger.debug(f"Games:\n{games_compare_str(response.games)}")
    assert response.query_summary is not None
    assert response.query_summary.total == 4
    last_game = None
    for game in response.games:
        logger.debug(game)
        if last_game is not None:
            assert game.release_date <= last_game.release_date
            if game.release_date == last_game.release_date:
                assert game.id > last_game.id
        last_game = game


async def test_game_list_sort_by_release_date_desc(session: AsyncSession):
    sort = schemas.GameListSort(
        release_date="desc"
    )
    response = await crud.game.get_game_list(session, sort=sort)
    logger.debug(response)
    logger.debug(f"Games:\n{games_compare_str(response.games)}")
    assert response.query_summary is not None
    assert response.query_summary.total == 4
    assert len(response.games) == response.query_summary.total
    last_game = None
    for game in response.games:
        logger.debug(game)
        if last_game is not None:
            assert game.release_date <= last_game.release_date
            if game.release_date == last_game.release_date:
                assert game.id > last_game.id
        last_game = game


async def test_game_list_sort_by_release_date_asc(session: AsyncSession):
    sort = schemas.GameListSort(
        release_date="asc"
    )
    response = await crud.game.get_game_list(session, sort=sort)
    logger.debug(response)
    logger.debug(f"Games:\n{games_compare_str(response.games)}")
    assert response.query_summary is not None
    assert response.query_summary.total == 4
    assert len(response.games) == response.query_summary.total
    last_game = None
    for game in response.games:
        logger.debug(game)
        if last_game is not None:
            assert game.release_date >= last_game.release_date
            if game.release_date == last_game.release_date:
                assert game.id > last_game.id
        last_game = game


async def test_crud_game_get_game_list_min_release_date(session: AsyncSession, test_data: None):
    min_release_date = datetime(2020, 1, 1, tzinfo=timezone.utc)

    filter = schemas.GameListFilter(
        min_release_date=min_release_date
    )

    response = await crud.game.get_game_list(session, filter=filter)
    logger.debug(f"Games:\n{games_compare_str(response.games)}")
    assert response.query_summary is not None
    assert response.query_summary.total > 0
    for game in response.games:
        assert game.release_date >= min_release_date


async def test_crud_game_get_game_list_max_release_date(session: AsyncSession, test_data: None):
    max_release_date = datetime(2020, 1, 1, tzinfo=timezone.utc)

    filter = schemas.GameListFilter(
        max_release_date=max_release_date
    )

    response = await crud.game.get_game_list(session, filter=filter)
    logger.debug(f"Games:\n{games_compare_str(response.games)}")
    assert response.query_summary is not None
    assert response.query_summary.total > 0
    for game in response.games:
        assert game.release_date <= max_release_date


async def test_crud_game_get_game_list_min_max_release_date(session: AsyncSession, test_data: None):
    min_release_date = datetime(2019, 1, 1, tzinfo=timezone.utc)
    max_release_date = min_release_date + timedelta(days=365)

    filter = schemas.GameListFilter(
        min_release_date=min_release_date,
        max_release_date=max_release_date
    )

    response = await crud.game.get_game_list(session, filter=filter)
    logger.debug(f"Games:\n{games_compare_str(response.games)}")
    assert response.query_summary is not None
    assert response.query_summary.total > 0
    for game in response.games:
        assert game.release_date >= min_release_date
        assert game.release_date <= max_release_date


async def test_crud_game_get_game_list_min_max_release_date_sort_release_date_asc(session: AsyncSession,
                                                                                  test_data: None):
    min_release_date = datetime(2018, 1, 1, tzinfo=timezone.utc)
    max_release_date = min_release_date + timedelta(days=2000)

    filter = schemas.GameListFilter(
        min_release_date=min_release_date,
        max_release_date=max_release_date
    )
    sort = schemas.GameListSort(
        release_date="asc"
    )

    response = await crud.game.get_game_list(session, filter=filter, sort=sort)
    logger.debug(f"Games:\n{games_compare_str(response.games)}")
    assert response.query_summary is not None
    assert response.query_summary.total > 0
    last_game = None
    for game in response.games:
        assert game.release_date >= min_release_date
        assert game.release_date <= max_release_date
        if last_game is not None:
            assert game.release_date >= last_game.release_date
            if game.release_date == last_game.release_date:
                assert game.id > last_game.id
        last_game = game


async def test_crud_game_get_game_list_min_max_release_date_sort_release_date_desc(session: AsyncSession,
                                                                                   test_data: None):
    min_release_date = datetime(2019, 1, 1, tzinfo=timezone.utc)
    max_release_date = min_release_date + timedelta(days=2000)

    filter = schemas.GameListFilter(
        min_release_date=min_release_date,
        max_release_date=max_release_date
    )
    sort = schemas.GameListSort(
        release_date="desc"
    )

    response = await crud.game.get_game_list(session, filter=filter, sort=sort)
    logger.debug(f"Games:\n{games_compare_str(response.games)}")
    assert response.query_summary is not None
    assert response.query_summary.total > 0
    last_game = None
    for game in response.games:
        assert game.release_date >= min_release_date
        assert game.release_date <= max_release_date
        if last_game is not None:
            assert game.release_date <= last_game.release_date
            if game.release_date == last_game.release_date:
                assert game.id > last_game.id
        last_game = game

async def test_crud_game_get_game_list_cursor_without_sort(session, test_data: None):
    limit = 1

    response = await crud.game.get_game_list(session, limit=limit)
    logger.debug(f"Games:\n{games_compare_str(response.games)}")
    assert response.query_summary is not None
    assert response.query_summary.total > limit
    assert len(response.games) == limit

    its = int(response.query_summary.total / limit) - 1
    used_cursors = []
    last_iter = 0
    for i in range(its+20):
        used_cursors.append(response.cursor)
        response = await crud.game.get_game_list(session, limit=limit, cursor=response.cursor)
        logger.debug(f"Games:\n{games_compare_str(response.games)}")
        assert response.query_summary is None
        last_iter = i
        if response.cursor in used_cursors:
            break

    assert last_iter == its



async def test_crud_game_get_game_list_cursor_with_sort(session, test_data: None):
    limit = 1

    sort = schemas.GameListSort(
        release_date="asc"
    )

    response = await crud.game.get_game_list(session, limit=limit, sort=sort)
    logger.debug(f"Games:\n{games_compare_str(response.games)}")
    assert response.query_summary is not None
    assert response.query_summary.total > limit
    assert len(response.games) == limit

    its = int(response.query_summary.total / limit) - 1
    used_cursors = []
    last_iter = 0
    for i in range(its+5):
        used_cursors.append(response.cursor)
        response = await crud.game.get_game_list(session, limit=limit, sort=sort, cursor=response.cursor)

        logger.debug(f"Games:\n{games_compare_str(response.games)}")
        logger.debug(f"Cursor: {response.cursor}")
        assert response.query_summary is None
        last_iter = i
        if len(response.games) == 0:
            break

    assert last_iter == its