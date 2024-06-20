from fastapi import FastAPI

from server.settings import AppConfig

settings = AppConfig()

server = FastAPI(
    **settings.model_dump(),
    openapi_url="/openapi.json" if settings.debug else None
)