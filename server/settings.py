from typing import Dict, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class AppConfig(BaseConfig):
    
    title: str = None
    summary: str = None
    contact: Dict[str, str] = None
    debug: bool = True
    version: str = "0.1.0"
    terms_of_service: Optional[str] = None

class RedisSettings(BaseConfig):

    host: str = "localhost"
    port: int = 6379
    password: Optional[str] = None

    def get_redis_uri(self) -> str:
        return f"redis://{self.host}:{self.port}"
