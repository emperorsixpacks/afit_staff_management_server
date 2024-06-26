from __future__ import annotations
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="allow")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserSchema(BaseSchema):
    # user_id: UUID
    first_name: str
    last_name: str
    email: str
    phone_number: str
    mobile_network: str
    state: str
    lga: str
    ward: str
    password_hash: str


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
