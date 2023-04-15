from datetime import datetime
from typing import Any, List, Optional, Dict, Tuple, Literal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/{id}", response_model=schemas.Game)
async def read_game(
        *,
        db: AsyncSession = Depends(deps.get_session),
        id: int
) -> Any:
    """
    Get game by ID.
    """
    game = await crud.game.get(db=db, id=id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@router.delete("/{id}", response_model=schemas.Game)
async def delete_game(
        *,
        db: AsyncSession = Depends(deps.get_session),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete game by ID.
    """
    game = await crud.game.get(db=db, id=id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    crud.game.remove(db=db, id=id)
    return game


@router.get("/", response_model=schemas.GameListResponse)
async def read_games(*,
                     db: AsyncSession = Depends(deps.get_session),
                     limit: int = 100,
                     offset: int = 0,
                     num_reviews: Optional[Literal['asc', 'desc']] = None,
                     score: Optional[Literal['asc', 'desc']] = None,
                     release_date: Optional[Literal['asc', 'desc']] = None,
                     name: Optional[str] = None,
                     min_num_reviews: Optional[int] = None,
                     max_num_reviews: Optional[int] = None,
                     min_score: Optional[float] = None,
                     max_score: Optional[float] = None,
                     min_release_date: Optional[datetime] = None,
                     max_release_date: Optional[datetime] = None,
                     categories: Optional[str] = None,
                     developers: Optional[str] = None
                     ) -> schemas.GameListResponse:
    """
    Get list of games.
    """
    sort = schemas.GameListSort(
        num_reviews=num_reviews,
        score=score,
        release_date=release_date
    )
    filter = schemas.GameListFilter(
        name=name,
        min_num_reviews=min_num_reviews,
        max_num_reviews=max_num_reviews,
        min_score=min_score,
        max_score=max_score,
        min_release_date=min_release_date,
        max_release_date=max_release_date,
        categories=categories.split(',') if categories else None,
        developers=developers.split(',') if developers else None
    )
    print(f"filter: {filter}")
    glist = await crud.game.get_game_list(db, limit=limit, offset=offset, filter=filter, sort=sort)
    return glist


# update game by id
@router.put("/{id}", response_model=schemas.Game)
async def update_game(
        *,
        db: AsyncSession = Depends(deps.get_session),
        id: int,
        game_in: schemas.GameUpdate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update game by ID.
    """
    game = await crud.game.get(db=db, id=id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    game = await crud.game.update(db=db, db_obj=game, obj_in=game_in)
    return game


@router.post("/", response_model=schemas.Game, status_code=201)
async def create_game(
        *,
        db: AsyncSession = Depends(deps.get_session),
        game_in: schemas.GameCreate,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new game.
    """
    game = await crud.game.get_by_name(db, name=game_in.name)
    if game:
        raise HTTPException(status_code=400, detail="Game already exists")
    game = await crud.game.create_from_source(db=db, obj_in=game_in, source_id=99, source_game_id='666')
    return game


@router.get("/{id}/sources", response_model=List[schemas.Source])
async def get_sources(*,
                      db: AsyncSession = Depends(deps.get_session),
                      id: int) -> Any:
    """
    Get all sources for a game.
    """
    sources = await crud.game.get_sources(db, game_id=id)
    return sources


@router.get("/{id}/summary/v2/{time_interval}", response_model=schemas.ReviewsSummaryV2)
async def get_summary_v2(*,
                         db: AsyncSession = Depends(deps.get_session),
                         id: int,
                         time_interval: str = "day"):
    # validate time interval
    # allowed_time_intervals = ["30 minutes",
    #                           "1 hour", "2 hours", "6 hours", "12 hours",
    #                           "1 day", "1 week", "1 month", "1 year"]
    allowed_time_intervals = ["hour", "day", "week", "month", "year"]
    if time_interval not in allowed_time_intervals:
        raise HTTPException(status_code=400, detail=f"Invalid time interval. Possible values: {allowed_time_intervals}")
    # get recent model
    result = await db.execute(select(models.Aspect.model_id, func.count(models.Aspect.id))
                             .group_by(models.Aspect.model_id)
                             .order_by(func.count(models.Aspect.id).desc()).limit(1))
    model_id = result.scalars().first()
    # get summary
    summary = await crud.review.get_summary_v2(db, game_id=id, time_interval=time_interval, model=model_id)
    return summary


@router.get("/{id}/summary/aspects", response_model=schemas.AspectsSummary)
async def get_aspect_summary(*,
                             db: AsyncSession = Depends(deps.get_session),
                             id: int) -> schemas.AspectsSummary:
    # get recent model
    result = await db.execute(select(models.Aspect.model_id, func.count(models.Aspect.id))
                              .group_by(models.Aspect.model_id)
                              .order_by(func.count(models.Aspect.id).desc()).limit(1))
    model_id = result.scalars().first()
    summary = await crud.review.get_aspect_summary_by_category_and_sources(db, game_id=id, model=model_id)
    return summary


@router.get("/search/", response_model=List[str])
async def get_name_matches(*,
                           db: AsyncSession = Depends(deps.get_session),
                           name: str,
                           limit: int = 10
                           ) -> List[str]:
    matches = await crud.game.get_matches(db, name=name, limit=limit)
    return matches


@router.get("/search/developers", response_model=List[schemas.Developer])
async def get_developers(*, db: AsyncSession = Depends(deps.get_session), name: str = None) -> List[schemas.Developer]:
    if name is None:
        objs = await crud.developer.get_multi_by_num_games(db, limit=10)
    else:
        objs = await crud.developer.get_multi_by_name(db, name=name)
    return objs


@router.get("/search/categories", response_model=List[schemas.Category])
async def get_categories(*, db: AsyncSession = Depends(deps.get_session), name: str = None) -> List[schemas.Category]:
    if name is None:
        objs = await crud.category.get_multi_by_num_games(db, limit=10)
    else:
        objs = await crud.category.get_multi_by_name(db, name=name)
    return objs
