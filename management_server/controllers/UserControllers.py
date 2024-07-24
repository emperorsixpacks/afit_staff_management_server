from uuid import UUID
from typing import Self, Dict

from fastapi import status
from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict
from tortoise.transactions import in_transaction

from management_server.schemas import UserSchema, StaffSchema
from management_server.models import UserModel, StaffModel
from management_server.controllers.DeparmentControllers import DepartmentController
from management_server.utils import verify_password
from management_server.exceptions import InvalidCredentialsError, InvalidRequestError
from management_server.controllers.base import BaseController


class UserController(BaseController):
    model_config = ConfigDict(extra="allow")
    email: EmailStr | None = Field(default=None)
    user_id: UUID | None = Field(default=None)

    @model_validator(mode="after")
    def check_fileds(self) -> Self:
        if self.email is None and self.user_id is None:
            raise ValueError(
                "email and user_id can not be None, pass atleast one argument for one"
            )
        return self

    def __get_user_search_key(self) -> Dict[str, str]:
        return {
            key: value
            for key, value in self.model_dump(exclude_none=True).items()
            if value is not None and key in ["email", "user_id"]
        }

    async def get_user(self):
        user = await UserModel.get_or_none(**self.__get_user_search_key())
        return UserSchema.model_validate(user.__dict__) if user else None

    @classmethod
    async def _create(cls, form_data: Dict[str, str]) -> StaffSchema:
        user_schema = UserSchema.model_validate(form_data)
        staff_schema = StaffSchema(
            user=user_schema, department_id=form_data.get("department_id")
        )
        async with in_transaction() as connection:
            if await UserModel.exists(email=user_schema.email, using_db=connection):
                raise InvalidRequestError(
                    detail="A staff with this email already exists",
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                )
            created_user = await UserModel.create(
                **user_schema.model_dump(exclude_unset=True, exclude_none=True),
                using_db=connection,
            )
            department = await DepartmentController(
                department_id=staff_schema.department_id
            ).get_department(using_db=connection)
            if department is None:
                raise InvalidRequestError(
                    detail=f"Invalid Department with id {staff_schema.department_id}",
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                )
            new_staff = await StaffModel.create(
                user_id=created_user.user_id, department_id=department.department_id, using_db=connection
            )
           
            return StaffSchema(
                department_id=department.department_id,
                staff_id=new_staff.staff_id,
                user=UserSchema.model_validate(created_user.__dict__),
            )

    def __str__(self) -> str:
        return "User"


class AuthController(BaseModel):
    email: EmailStr
    password: str

    async def validate_password(self):
        hash_user_password = await UserModel.get_or_none(email=self.email)
        if not verify_password(hash_user_password, self.password):
            raise InvalidCredentialsError(detail="Invalid email or password")
        return True
