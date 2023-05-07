"""
Created by Frantisek Sabol
"""
from typing import Any, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
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


@router.get("/", response_model=schemas.ReviewListResponse)
async def read_reviews(
        *,
        db: AsyncSession = Depends(deps.get_session),
        game_id: Optional[int] = None,
        aspect: Optional[str] = None,
        source: Optional[str] = None,
        polarity: Optional[str] = None,
        model: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
) -> Any:
    """
    Read all reviews.
    """
    model = model.split(",") if model else None
    aspects = aspect.split(",") if aspect else []
    aspects = [aspect for aspect in aspects if aspect in
               ('overall', 'gameplay', 'performance_bugs', 'price', 'audio_visuals', 'community')]
    aspects = aspects if len(aspects) > 0 else None

    polarities = polarity.split(",") if polarity else []
    polarities = [polarity for polarity in polarities if polarity in ('positive', 'negative', 'neutral')]
    polarities = polarities if len(polarities) > 0 else None


    result = await crud.review.get_multi_with_aspects(db,
                                                      model_ids=model,
                                                      game_id=game_id,
                                                      aspects=aspects,
                                                      polarities=polarities,
                                                      offset=skip,
                                                      limit=limit)

    return result



@router.get("/summary/", response_model=schemas.ReviewsSummary)
async def get_summary(db: AsyncSession = Depends(deps.get_session),
                      game_id: Optional[int] = None,
                      source_ids: Optional[List[int]] = None):
    summary = await crud.review.get_summary(db,
                                            game_id=game_id,
                                            time_interval="day")
    return summary


@router.get("/{id}/aspects/", response_model=List[schemas.Aspect])
async def get_aspects(db: AsyncSession = Depends(deps.get_session),
                      id: int = None):
    review = await crud.review.get_with_aspects(db=db, id=id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review.aspects
