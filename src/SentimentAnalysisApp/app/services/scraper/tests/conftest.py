from typing import AsyncGenerator

import pytest
import asyncio
import os

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core import config
from db.base_class import Base
from db.session import async_engine, async_session


