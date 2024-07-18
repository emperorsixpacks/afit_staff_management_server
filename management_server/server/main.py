from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from tortoise.contrib.fastapi import RegisterTortoise
from management_server.settings import AppConfig, DBSettings
from management_server.routers import staff_routers, admin_routers, auth_routers
from management_server.exceptions import (
    ServerFailureError,
    InvalidCredentialsError,
    InvalidRequestError,
)
from management_server.exceptions.handlers import (
    _invalid_credentials_handler,
    _invalid_request_error_handler,
    _sever_failed_error_handler,
)

db_settings = DBSettings()

settings = AppConfig(
    title="Staff Management Server",
    summary="Staff Management Server",
    contact={
        "name": "Staff Management Server",
        "url": "https://github.com/emperorsixpacks/afit_staff_management_server/",
    },
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # app startup
    async with RegisterTortoise(app, config_file=db_settings.tortoise_config):
        yield


server = FastAPI(
    **settings.model_dump(),
    openapi_url="/openapi.json" if settings.debug else None,
    lifespan=lifespan
)

server.add_exception_handler(InvalidRequestError, _invalid_request_error_handler)
server.add_exception_handler(ServerFailureError, _sever_failed_error_handler)
server.add_exception_handler(InvalidCredentialsError, _invalid_credentials_handler)

server.include_router(staff_routers.router)
server.include_router(admin_routers.router)
server.include_router(auth_routers.router)
