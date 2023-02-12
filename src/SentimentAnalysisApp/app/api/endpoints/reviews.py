from typing import Any, List, Optional

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
        game_id: Optional[int] = None,
        source_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
) -> Any:
    """
    Read all reviews.
    """
    reviews = await crud.review.get_multi_by_game_and_source(
        db,
        source_id=source_id,
        game_id=game_id,
        offset=skip,
        limit=limit
    )
    return reviews


@router.get("processed/", response_model=List[schemas.ReviewWithAspects])
async def read_processed_reviews(db: AsyncSession = Depends(deps.get_session),
                                 source_id: Optional[int] = None,
                                 game_id: Optional[int] = None,
                                 limit: int = 100, skip: int = 0):
    reviews = await crud.review.get_multi_with_aspects(db,
                                                       source_id=source_id,
                                                       game_id=game_id,
                                                       offset=skip,
                                                       limit=limit)
    return reviews
