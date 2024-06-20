from fastapi import FastAPI

from src.server.settings import AppConfig

settings = AppConfig(
    title="Staff Management Server",
    summary="Staff Management Server",
    contact={
        "name": "Staff Management Server",
        "url": "https://github.com/emperorsixpacks/afit_staff_management_server/"
    }
)

server = FastAPI(
    **settings.model_dump(),
    openapi_url="/openapi.json" if settings.debug else None
)