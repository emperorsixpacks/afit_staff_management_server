from __future__ import annotations
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class BaseSchema(BaseModel):
    created_at: datetime
    updated_at: datetime


class UserSchema(BaseSchema):
    user_id: UUID
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
    username: str
    password_hash: str
