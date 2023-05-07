"""
https://fastapi-users.github.io/fastapi-users/configuration/routers/
fastapi_users is defined in deps, because it also
includes useful dependencies.
"""

from fastapi import APIRouter

from app.api.deps import fastapi_users
from app.core import security
from app.api.endpoints import analyzer, games, reviews, sources

api_router = APIRouter()
api_router.include_router(
    fastapi_users.get_auth_router(security.AUTH_BACKEND),
    prefix="/auth/jwt",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_register_router(),
    prefix="/auth",
    tags=["auth"],
)
api_router.include_router(
    fastapi_users.get_users_router(),
    prefix="/users",
    tags=["users"],
)

api_router.include_router(
    analyzer.router,
    prefix="/analyzer",
    tags=["analyzer"]
)

api_router.include_router(
    games.router,
    prefix="/games",
    tags=["games"]
)

api_router.include_router(
    reviews.router,
    prefix="/reviews",
    tags=["reviews"]
)

api_router.include_router(
    sources.router,
    prefix="/sources",
    tags=["sources"]
)
