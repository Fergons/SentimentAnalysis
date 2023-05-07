"""
Created by Frantisek Sabol
"""
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.services.analyzer import get_extractor, extract_aspects, clean
from app.api import deps

router = APIRouter()


@router.post("/analyze")
async def analyze_text(
        *,
        db: AsyncSession = Depends(deps.get_session),
        review: schemas.ReviewCreate,
        model: str = None,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Uses service app.services.analyzer to extract aspects from text
    """
    extractor = get_extractor(model_name=model)
    results = extract_aspects(text=clean(review.text), language=review.language, extractor=extractor)
    # return original text and result aspect and sentiment for result in results
    review = await crud.review.create(db=db, obj_in=review)
    aspects = []
    for result in results:
        for term, polarity, confidence in zip(result["aspect"], result["sentiment"], result["confidence"]):
            aspect = await crud.aspect.create_for_review(db=db,
                                                         obj_in=schemas.AspectCreate(
                                                             term=term,
                                                             polarity=polarity,
                                                             confidence=confidence),
                                                         review_id=review.id)
            aspects.append({"term": term, "polarity": polarity})

    return {
        "text": review.text,
        "aspects": aspects
    }
