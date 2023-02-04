from typing import Any, List

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


@router.get("/", response_model=List[schemas.Game])
async def read_games(
    *,
    db: AsyncSession = Depends(deps.get_session),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve games.
    """
    games = await crud.game.get_multi(db, offset=skip, limit=limit)
    return games

#update game by id
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
    game = await crud.game.create_from_source(db=db, obj_in=game_in, source_id=99, source_game_id=666)
    return game