from __future__ import annotations
from uuid import UUID
from typing import Optional, Self
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator,field_validator, field_serializer

from management_server.utils.model_helpers import EmailString
from management_server.utils.validators import phone_number_vaidator


class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="allow")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserSchema(BaseSchema):
    user_id: Optional[UUID] = None
    first_name: str
    last_name: str
    email: EmailString
    phone_number: str
    state: str
    lga: str
    ward: str
    mobile_network: str | None = Field(default=None)

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


class BaseStaffSchema(BaseSchema):
    staff_id: str
    user: UserSchema


class StaffSchema(BaseStaffSchema):
    department: str


class AdminShema(BaseSchema):
    ...
