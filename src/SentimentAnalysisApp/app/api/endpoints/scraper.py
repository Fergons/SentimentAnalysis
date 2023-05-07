"""
Created by Frantisek Sabol
"""
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.services.scraper import DBScraper
from app.services.scraper.constants import SourceName
from app.api import deps
from services.scraper import SteamScraper, GamespotScraper, DoupeScraper

router = APIRouter()


@router.post("/scrape")
def scrape_reviews(
        *,
        db: AsyncSession = Depends(deps.get_session),
        source: str,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Uses service app.services.scraper to scrape reviews from selected source
    """
    _Scraper = None
    # check if user is priviliged
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if SourceName.STEAM.value == source:
        _Scraper = SteamScraper
    elif SourceName.GAMESPOT.value == source:
        _Scraper = GamespotScraper
    elif SourceName.DOUPE.value == source:
        _Scraper = DoupeScraper
    elif SourceName.METACRITIC.value == source:
        raise HTTPException(status_code=400, detail="Not Implemented")
    else:
        raise HTTPException(status_code=400, detail="Invalid source")

    async with _Scraper() as scraper:
        scraper = await DBScraper.create(scraper=scraper, session=db)


@router.post("/sources")
def get_scrapable_sources() -> List[str]:
    """
    Returns list of sources that can be scraped
    """
    # return [source.value for source in SourceName]
    return ["steam", "doupe", "gamespot"]