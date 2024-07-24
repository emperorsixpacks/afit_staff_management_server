from typing import Dict
from uuid import UUID

from pydantic import field_validator
from tortoise.transactions import in_transaction

from management_server.models import DepartmentModel, AdminModel
from management_server.exceptions import InvalidRequestError
from management_server.schemas import DepartmentSchema
from management_server.controllers.base import BaseController


class DepartmentController(BaseController):
    department_id: UUID

    @classmethod
    @field_validator("department_id", mode="after")
    async def validate_department_id(cls, value):
        if not await DepartmentModel.exists(department_id=value):
            raise InvalidRequestError(
                detail=f"Department with id {value} does not exist"
            )
        return value

    async def get(self, using_db=None) -> DepartmentModel | None:
        department = await DepartmentModel.get_or_none(
            department_id=self.department_id, using_db=using_db
        )
        return department or None

    @classmethod
    async def _create(cls, form_data: Dict[str, str]):
        department_schema = DepartmentSchema.model_validate(form_data)
        async with in_transaction() as connection:
            if department_schema.department_head_id is not None:
                admin = AdminModel.exists(
                    staff_id=department_schema.department_head_id
                )
                if not admin:
                    raise InvalidRequestError(
                        detail=f"Staff with ID {department_schema.department_head_id} does not exist",
                        status_code=404,
                )

            created_department = await DepartmentModel.create(
                **department_schema.model_dump(exclude_none=True, exclude_unset=True),
                using_db=connection,
            )

            return DepartmentSchema.model_validate(created_department.__dict__)
        
    async def exists(self) -> bool:
        return await DepartmentModel.exists(department_id=self.department_id)
    
    def __name__(self) -> str:
        return "Department"
