from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
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
                     cursor: Optional[int] = None,
                     filter: Optional[schemas.GameListFilter] = None) -> schemas.GameListResponse:
    """
    Get list of games.
    """
    glist = await crud.game.get_game_list(db, limit=limit, cursor=cursor, filter=filter)
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

    summary = await crud.review.get_summary_v2(db, game_id=id, time_interval=time_interval)
    return summary
