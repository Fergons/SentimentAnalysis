from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.services.scraper import DBScraper
from app.api import deps

router = APIRouter()
