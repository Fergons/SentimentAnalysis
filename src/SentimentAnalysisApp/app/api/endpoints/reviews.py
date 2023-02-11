from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/{id}", response_model=schemas.Review)
async def read_review(
        *,
        db: AsyncSession = Depends(deps.get_session),
        id: int
) -> Any:
    """
    Get game by ID.
    """
    review = await crud.review.get(db=db, id=id)
    if not review:
        raise HTTPException(status_code=404, detail="Game not found")
    return review


@router.get("/", response_model=List[schemas.Review])
async def read_reviews(
        *,
        db: AsyncSession = Depends(deps.get_session),
        skip: int = 0,
        limit: int = 100
) -> Any:
    """
    Get game by ID.
    """
    review = await crud.review.get(db=db, id=id)
    if not review:
        raise HTTPException(status_code=404, detail="Game not found")
    return review


@router.get("/", response_model=List[schemas.Review])
async def read_reviews_by_game(
        *,
        db: AsyncSession = Depends(deps.get_session),
        skip: int = 0,
        limit: int = 100,
        game_id: int = 0
):
    """
    Get reviews for a game.
    """
    reviews = await crud.review.get_multi_by_game(db, game_id=game_id, offset=skip, limit=limit)
    return reviews


@router.get("/", response_model=List[schemas.ReviewWithAspects])
async def read_processed_reviews(db: AsyncSession = Depends(deps.get_session), source_id: int = None, game_id: int = None, limit: int = 100, skip: int = 0):
    reviews = await crud.review.get_multi_with_aspects(db, source_id=source_id, game_id=game_id, offset=skip, limit=limit)
    return reviews
