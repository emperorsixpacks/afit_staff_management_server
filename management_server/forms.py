from dataclasses import dataclass
from fastapi import Form

@dataclass
class UserCreateForm:
    first_name: str = Form(...)
    last_name: str = Form(...)
    email: str = Form(...)
    phone_number: str = Form(...)
    state: str = Form(...)
    lga: str = Form(...)
    ward: str = Form(...)



@dataclass
class LoginForm:
    email: str = Form()
    password: str = Form()