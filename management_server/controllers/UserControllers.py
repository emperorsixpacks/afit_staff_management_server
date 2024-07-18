from uuid import UUID
from typing import Self, Dict

from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict

from management_server.schemas import UserSchema
from management_server.models import UserModel
from management_server.utils import verify_password
from management_server.exceptions import InvalidCredentialsError

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

    async def get_user(self):
        user = await UserModel.get_or_none(**self.__get_user_search_key())
        return UserSchema.model_validate(user.__dict__) if user else None
    
    @classmethod
    async def create_new_user(cls, form_data:UserSchema):
        created_user = await UserModel.create(**form_data.model_dump(exclude_unset=True, exclude_none=True))
        return UserSchema.model_validate(created_user.__dict__)


class AuthController(BaseModel):
    email: EmailStr
    password: str

    async def validate_password(self):
        hash_user_password = await UserModel.get_or_none(email=self.email).
        if not verify_password(hash_user_password, self.password):
            raise InvalidCredentialsError(detail="Invalid email or password")
        return True
        