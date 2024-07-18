import os
from typing import Dict, Optional, Union

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import FilePath, field_validator

from management_server.constants import APP_BASE_URL
from management_server.helpers import DBType


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
    
class DBSettings(BaseConfig):
    database_name: str
    database_hostname: Optional[str] = None
    database_port: Optional[Union[str, int]] = None
    database_password: Optional[str] = None
    database_username: Optional[str] = None
    secret_key: Optional[str] = None
    database_type: DBType = DBType.SQLITE
    tortoise_config: Optional[FilePath | None ] = None

    def __post_init__(self):
        if self.database_type not in [i.value for i in DBType]:
            raise ValueError(
                "Invalid database type, should be one of sqlite, postgresql, mysql"
            )

    @property
    def database_url(self):
        if not os.path.exists(f"{APP_BASE_URL}/{self.database_name}.sqlite3"):
            os.makedirs(f"{APP_BASE_URL}", exist_ok=True)
        if self.database_type == DBType.SQLITE:
            return f"{self.database_type}:///{APP_BASE_URL}/{self.database_name}.sqlite3"
        return f"{self.database_type}://{self.database_username}:{self.database_password}@{self.database_hostname}:{self.database_port}/{self.database_name}"
    
    @field_validator("tortoise_config", mode="before")
    @classmethod
    def check_if_none(cls, value):
        if value == "NONE" or value == "" or not os.path.exists(value):
            return None
        return value

class RedisSettings(BaseConfig):
    redis_port: str = "6379"
    redis_host: str = "localhost"