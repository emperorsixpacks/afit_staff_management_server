from dataclasses import dataclass
from fastapi import Form


email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


@dataclass
class StaffCreateForm:
    first_name: str = Form(min_length=3, max_length=50, serialization_alias="first-name")
    last_name: str = Form(min_length=3, max_length=50, serialization_alias="last-name")
    email: str = Form(regex=email_pattern, min_length=15, max_length=50)
    phone_number: str = Form(max_length=11, min_length=11, serialization_alias="phone-number")
    state: str = Form(...)
    lga: str = Form(...)
    ward: str = Form(...)
    department_id: str = Form(serialization_alias="department-id")



@dataclass
class LoginForm:
    email: str = Form()
    password: str = Form()


@dataclass
class DepartmentCreateForm:
    name: str = Form(...)
    short_name: str = Form(...)
    description: str = Form(...)
    department_head_id: str | None = Form(serialization_alias="deparment-head-id", default=None)
