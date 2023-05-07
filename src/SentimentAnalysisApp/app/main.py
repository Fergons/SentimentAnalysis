"""
Created by Frantisek Sabol
Main FastAPI app instance declaration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core import config

app = FastAPI(
    title=config.settings.PROJECT_NAME,
    version=config.settings.VERSION,
    description=config.settings.DESCRIPTION,
    openapi_url="/openapi.json",
    docs_url="/",
)

# Set all CORS enabled origins
if config.settings.BACKEND_CORS_ORIGINS:
    if "DEV" == config.settings.ENVIRONMENT or "PYTEST" == config.settings.ENVIRONMENT:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
    else:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in config.settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

app.include_router(api_router)
