from __future__ import annotations
from uuid import UUID
from typing import Optional, Self, Dict, List
from datetime import datetime
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
    field_serializer,
)

from management_server.utils.model_helpers import EmailString
from management_server.utils.validators import phone_number_vaidator


class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="allow")
    created_at: Optional[datetime] = Field(serilization_alias="created-at", default=None)
    updated_at: Optional[datetime] = Field(serilization_alias="updated-at", default=None)


class UserSchema(BaseSchema):
    model_config = ConfigDict(extra="ignore")
    user_id: Optional[UUID] = Field(serialization_alias="user-id", default=None)
    first_name: str = Field(serialization_alias="first-name")
    last_name: str = Field(serialization_alias="last-name")
    phone_number: str = Field(serialization_alias="phone-number")
    mobile_network: str | None = Field(default=None, alias="mobile-network")
    email: EmailString
    state: str
    lga: str
    ward: str

    @model_validator(mode="before")
    def filter_extra_fields(cls, values):
        valid_fields = {field: values[field] for field in cls.model_fields if field in values}
        return valid_fields

    @model_validator(mode="after")
    def validate_phone_number(self) -> Self:
        mobile_network = phone_number_vaidator(self.phone_number)
        if mobile_network is None:
            raise ValueError(f"Invalid Phone number {self.phone_number}")
        self.mobile_network = mobile_network
        return self

    @field_serializer("user_id", when_used="always")
    def serialize_id(self, user_id: UUID, _info):
        """
        Serialize the given user ID to a string representation.

        :param user_id: The user ID to be serialized.
        :type user_id: uuid_pkg.UUID
        :param _info: Additional information about the serialization process.
        :type _info: Any
        :return: The serialized string representation of the user ID.
        :rtype: str
        """
        return str(user_id)


class DepartmentSchema(BaseSchema):
    department_id: UUID
    name: str
    short_name: str
    description: str
    department_head: AdminShema


class StaffSchema(BaseModel):
    user:UserSchema
    department_id:str = Field(serialization_alias="department-id")
    staff_id: str = Field(serialization_alias="staff-id")

    @model_validator(mode="before")
    def filter_extra_fields(cls, values):
        valid_fields = {field: values[field] for field in cls.model_fields if field in values}
        return valid_fields

class AdminShema(BaseSchema): ...

class Sessions(BaseSchema):
    name: str
    device_name:str

class UserInCache(BaseModel):
    user: UserSchema | Dict[str, str]
    sessions: List[Sessions]

    @field_serializer("user", when_used="json")
    def serialize_user_field(user:UserSchema):
        return user.model_dump_json()
    
    @field_serializer("sessions", when_used="json")
    def serialize_sessions_field(sessions:List[Sessions]):
        return [session.model_dump_json() for session in sessions]