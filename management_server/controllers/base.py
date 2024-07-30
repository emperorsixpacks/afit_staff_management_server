from typing import Dict, Self
from tortoise.exceptions import OperationalError
from pydantic import BaseModel
from management_server.exceptions import ServerFailureError


class BaseController(BaseModel):
    
    async def get(self, return_model: bool = False) -> Self:
        ...

    @classmethod
    async def create(cls, form_data: Dict[str, str]):
        try:
            return await cls._create(form_data=form_data)
        except OperationalError as e:
            print(f"error {e}")
            raise ServerFailureError(detail=f"Could not create {cls.__name__}") from e
    
    