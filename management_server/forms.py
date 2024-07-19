from dataclasses import dataclass
from fastapi import Form

email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


@dataclass
class StaffCreateForm:
    first_name: str = Form(min_length=3, max_length=50)
    last_name: str = Form(min_length=3, max_length=50)
    email: str = Form(regex=email_pattern, min_length=15, max_length=50)
    phone_number: str = Form(max_length=11, min_length=11)
    state: str = Form(...)
    lga: str = Form(...)
    ward: str = Form(...)
    department_id: str = Form(...)



@dataclass
class LoginForm:
    email: str = Form()
    password: str = Form()