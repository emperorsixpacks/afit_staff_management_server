from uuid import UUID
from typing import Self, Dict

from fastapi import status
from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict
from tortoise.transactions import in_transaction

from management_server.schemas import UserSchema, StaffSchema, UserInCache
from management_server.models import UserModel, StaffModel, AdminModel
from management_server.controllers.DeparmentControllers import DepartmentController
from management_server.utils import verify_password
from management_server.exceptions import InvalidCredentialsError, InvalidRequestError
from management_server.controllers.base import BaseController
from management_server.redis_cache import Redis


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

    def _get_search_key(self) -> Dict[str, str]:
        return {
            key: value
            for key, value in self.model_dump(exclude_none=True).items()
            if value is not None and key in ["email", "user_id"]
        }

    async def get(self, return_model: bool = False):
        user = await UserModel.get_or_none(**self._get_search_key())
        if return_model:
            return user if user else None
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
            ).get(using_db=connection)
            if department is None:
                raise InvalidRequestError(
                    detail=f"Invalid Department with id {staff_schema.department_id}",
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                )
            new_staff = await StaffModel.create(
                user_id=created_user.user_id,
                department_id=department.department_id,
                using_db=connection,
            )

            new_staff_schema = StaffSchema(
                department_id=department.department_id,
                staff_id=new_staff.staff_id,
                user=UserSchema.model_validate(created_user.__dict__),
            )
            user_in_cahce = UserInCache(staff=new_staff_schema)
            await Redis.create_key(key=new_staff.staff_id, data=user_in_cahce)

            return new_staff_schema

    async def exists(self) -> bool:
        return await UserModel.exists(**self._get_search_key())

    def __str__(self) -> str:
        return "User"


class BaseStaffController(BaseController):
    id: UUID | None = Field(default=None)
    staff_id: str | None = Field(default=None)
    fields: Dict[str, str] | None = Field(default=None)

    @model_validator(mode="after")
    def check_fileds(self) -> Self:
        if self.id is None and self.staff_id is None:
            raise ValueError(
                "id and staff_id can not be None, pass atleast one argument for one"
            )
        return self

    def _get_search_key(self) -> Dict[str, str]:
        return {
            key: value
            for key, value in self.model_dump(exclude_none=True).items()
            if value is not None and key in ["id", "staff_id"]
        }

    async def update(self):
        if self.fields is None:
            raise ValueError("Field cannnot be None")
        if not await self.exists():
            raise InvalidRequestError(
                detail="Staff with this ID does not exist", status_code=404
            )
        staff = await self.get(return_model=True)
        print(staff)
        user = await UserController(email=staff.user.email).get(return_model=True)
        updated_user = user.update_from_dict(self.fields)
        return  UserSchema.model_validate(updated_user.__dict__)



class StaffController(BaseStaffController):

    async def get(self, return_model: bool = False):
        user = await StaffModel.get_or_none(**self._get_search_key())
        if return_model:
            return user if user else None
        return StaffSchema.model_validate(user.__dict__) if user else None

    async def exists(self) -> bool:
        return await StaffModel.exists(**self._get_search_key())


class AdminController(BaseStaffController):
    id: UUID | None = Field(default=None)
    staff_id: str | None = Field(default=None)

    async def get(self):
        user = await AdminModel.get_or_none(**self._get_search_key())
        return StaffSchema.model_validate(user.__dict__) if user else None

    async def exists(self) -> bool:
        print("pass")
        return await AdminModel.exists(**self._get_search_key())

    @classmethod
    async def _create(cls, form_data: Dict[str, str]) -> StaffSchema:
        async with in_transaction() as connection:
            if await UserController(user_id=form_data["user_id"]).exists():
                raise InvalidRequestError("A user with this ID already exists")
            created_admin = await AdminModel.create(**form_data, usin_db=connection)
            user = await UserController(user_id=form_data["user_id"]).get()
            return StaffSchema(
                department_id=form_data["department_id"],
                staff_id=created_admin.staff_id,
                user=UserSchema.model_validate(user.__dict__),
            )


class AuthController(BaseModel):
    email: EmailStr
    password: str

    async def validate_password(self):
        hash_user_password = await UserModel.get_or_none(email=self.email)
        if not verify_password(hash_user_password, self.password):
            raise InvalidCredentialsError(detail="Invalid email or password")
        return True

    # async def login(self):
