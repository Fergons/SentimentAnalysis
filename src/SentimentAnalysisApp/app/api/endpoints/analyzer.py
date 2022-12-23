from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.services.analyzer import get_extractor, extract_aspects, clean
from app.api import deps

router = APIRouter()


@router.post("/analyze")
def analyze_text(
        *,
        # db: Session = Depends(deps.get_session),
        review: schemas.ReviewCreate,
        model: str = None,
        # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Uses service app.services.analyzer to extract aspects from text
    """
    extractor = get_extractor(checkpoint_name=model)
    results = extract_aspects(text=clean(review.text), language=review.language, extractor=extractor)
    # return original text and result aspect and sentiment for result in results
    aspects = []
    for result in results:
        for term, polarity in zip(result["aspect"], result["sentiment"]):
            aspects.append({"term": term, "polarity": polarity})

    return {
        "text": review.text,
        "aspects": aspects
    }
