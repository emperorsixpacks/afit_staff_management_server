from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise
from management_server.server.settings import AppConfig, DBSettings

db_settings = DBSettings()

settings = AppConfig(
    title="Staff Management Server",
    summary="Staff Management Server",
    contact={
        "name": "Staff Management Server",
        "url": "https://github.com/emperorsixpacks/afit_staff_management_server/"
    }
)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # app startup
    async with RegisterTortoise(
        app,
        config_file=db_settings.tortoise_config
    ):
        yield

server = FastAPI(
    **settings.model_dump(),
    openapi_url="/openapi.json" if settings.debug else None,
    lifespan=lifespan
)


