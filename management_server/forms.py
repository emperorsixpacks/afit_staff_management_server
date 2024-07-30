from uuid import UUID
from dataclasses import dataclass

from fastapi import Form

email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


@dataclass
class StaffCreateForm:
    first_name: str = Form(min_length=3, max_length=50, alias="first-name")
    last_name: str = Form(min_length=3, max_length=50, alias="last-name")
    email: str = Form(regex=email_pattern, min_length=15, max_length=50)
    phone_number: str = Form(max_length=11, min_length=11, alias="phone-number")
    state: str = Form(...)
    lga: str = Form(...)
    ward: str = Form(...)
    department_id: str = Form(alias="department-id")


@dataclass
class AdminCreateForm:
    user_id: UUID = Form(alias="user-id")
    department_id: UUID = Form(alias="department-id")


@dataclass
class LoginForm:
    email: str = Form()
    password: str = Form()


@dataclass
class DepartmentCreateForm:
    name: str = Form(...)
    short_name: str = Form(...)
    description: str = Form(...)
    department_head_id: str | None = Form(alias="deparment-head-id", default=None)


@dataclass
class StaffUpdateForm:
    first_name: str | None = Form(
        default=None,
        min_length=3,
        max_length=50,
        alias="first-name",
        validation_alias="first-name",
    )
    last_name: str | None = Form(
        default=None,
        min_length=3,
        max_length=50,
        alias="last-name",
        validation_alias="last-name",
    )
    email: str | None = Form(
        default=None,
        regex=email_pattern,
        min_length=15,
        max_length=50,
        example="example@example.com",
    )
    phone_number: str | None = Form(
        default=None,
        max_length=11,
        min_length=11,
        alias="phone-number",
        validation_alias="phone-number",
        example="09000000001",
    )
    state: str | None = Form(default=None)
    lga: str | None = Form(default=None)
    ward: str | None = Form(default=None)
