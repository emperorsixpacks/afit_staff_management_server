from __future__ import annotations
from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator

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
    password_hash: str = Field(exclude=True)
    mobile_network: str| None = Field(exclude=True, default=None)

    @classmethod
    @field_validator("mobile_network", mode="after")
    def validate_phone_number(cls, value):
        mobile_network = phone_number_vaidator(value)
        if mobile_network is None:
            raise ValueError(f"Invalid Phone number {value}")
        return mobile_network




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
