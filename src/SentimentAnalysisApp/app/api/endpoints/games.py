from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/game", response_model=schemas.Game)
async def read_game(
    *,
    db: Session = Depends(deps.get_session),
    game_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get game by ID.
    """
    game = await crud.game.get(db=db, id=game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game


@router.delete("/game", response_model=schemas.Game)
async def delete_game(
    *,
    db: Session = Depends(deps.get_session),
    game_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete game by ID.
    """
    game = await crud.game.get(db=db, id=game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    crud.game.remove(db=db, id=game_id)
    return game


@router.get("/games", response_model=List[schemas.Game])
async def read_games(
    *,
    db: Session = Depends(deps.get_session),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve games.
    """
    games = await crud.game.get_multi(db, skip=skip, limit=limit)
    return games

