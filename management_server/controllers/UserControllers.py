from uuid import UUID
from typing import Self, Dict, TypeVar

from fastapi import status
from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict
from tortoise.transactions import atomic
from tortoise.exceptions import OperationalError

from management_server.schemas import UserSchema, StaffSchema
from management_server.models import UserModel, StaffModel, DepartmentModel
from management_server.utils import verify_password
from management_server.exceptions import (
    InvalidCredentialsError,
    InvalidRequestError,
    ServerFailureError,
)

FORM_DATA = TypeVar("FORM_DATA")


class UserController(BaseModel):
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

    @classmethod
    def _set_form_data(cls, form_data: FORM_DATA):
        cls._form_data = form_data
        return None

    @classmethod
    def _get_form_data(cls) -> FORM_DATA:
        return cls._form_data

    async def get_user(self):
        user = await UserModel.get_or_none(**self.__get_user_search_key())
        return UserSchema.model_validate(user.__dict__) if user else None

    @classmethod
    @atomic
    async def _create_new_staff(cls) -> StaffSchema:
        form_data = cls._get_form_data()
        if not await UserModel.exists(email=form_data.email):
            raise InvalidRequestError(
                detail="A staff with this email already exists",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )
        created_user = await UserModel.create(
            **form_data.model_dump(exclude_unset=True, exclude_none=True)
        )
        department = await DepartmentModel.get_or_none(
            department_id=form_data.department_id
        )
        if department is None:
            raise InvalidRequestError(
                detail=f"Invalid Department with id {form_data.department_id}",
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
            )
        new_staff = await StaffModel.create(user=created_user, department=department)
        return StaffSchema(
            department_id=department.department_id,
            staff_id=new_staff.staff_id,
            user=UserSchema.model_validate(created_user.__dict__),
        )

    @classmethod
    async def create_new_staff(cls, form_data: FORM_DATA):
        cls._set_form_data(form_data=form_data)
        try:
            await cls._create_new_staff()
        except OperationalError as e:
            print(f"error {e}")
            raise ServerFailureError(detail="Could not create user") from e


class AuthController(BaseModel):
    email: EmailStr
    password: str

    async def validate_password(self):
        hash_user_password = await UserModel.get_or_none(email=self.email)
        if not verify_password(hash_user_password, self.password):
            raise InvalidCredentialsError(detail="Invalid email or password")
        return True
