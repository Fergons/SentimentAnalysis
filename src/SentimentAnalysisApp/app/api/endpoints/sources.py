from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Source])
async def read_sources(
        *,
        db: AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    Get all review sources.
    """
    sources = await crud.source.get_all(db=db)
    return sources
