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

@router.get("/{source_id}", response_model=schemas.Source)
async def read_source(
        *,
        db: AsyncSession = Depends(deps.get_session),
        source_id: int,
) -> Any:
    """
    Get a single review source.
    """
    source = await crud.source.get(db=db, id=source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source

@router.post("/", response_model=schemas.Source)
async def create_source(
        *,
        db: AsyncSession = Depends(deps.get_session),
        user: models.User = Depends(deps.get_current_superuser),
        source_in: schemas.SourceCreate,
) -> Any:
    """
    Create a new review source.
    """
    if not user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    source = await crud.source.create(db=db, obj_in=source_in)
    return source


@router.put("/{source_id}", response_model=schemas.Source)
async def update_source(
        *,
        db: AsyncSession = Depends(deps.get_session),
        user: models.User = Depends(deps.get_current_superuser),
        source_id: int,
        source_in: schemas.SourceUpdate,
) -> Any:
    """
    Update a review source.
    """
    if not user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    source = await crud.source.get(db=db, id=source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    source = await crud.source.update(db=db, db_obj=source, obj_in=source_in)
    return source

@router.delete("/{source_id}", response_model=schemas.Source)
async def delete_source(
        *,
        db: AsyncSession = Depends(deps.get_session),
        user: models.User = Depends(deps.get_current_superuser),
        source_id: int,
) -> Any:
    """
    Delete a review source.
    """
    if not user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    source = await crud.source.get(db=db, id=source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    source = await crud.source.remove(db=db, id=source_id)
    return source