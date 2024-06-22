from __future__ import annotations
from pydantic import Field, ConfigDict, EmailStr
from email_validator import 

from management_server.models import BaseModel

class UserModel(BaseModel, table=True):
    """
    User model class
    """

    model_config = ConfigDict(
        extra="forbid", str_strip_whitespace=True, use_enum_values=True
    )
    first_name: str = Field(max_length=20, min_length=3, nullable=False)
    last_name: str = Field(max_length=20, min_length=3, nullable=False)
    email: str = Field(unique=True, nullable=False, max_length=255, min_length=10)
    phone_number: str = Field(unique=True, nullable=False, min_length=11, max_length=11)
    state: str = Field(default=None, max_length=50, nullable=False)
    lga: str = Field(default=None, max_length=50, nullable=False)
    ward: str = Field(default=None, max_length=50, nullable=False)

class StaffModel(BaseModel, table=True):
    pass

class AdminModel(BaseModel, table=True):
    pass