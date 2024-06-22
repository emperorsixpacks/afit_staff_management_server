from __future__ import annotations
from typing import Dict
from pydantic import ConfigDict, model_validator

from sqlmodel import Field, Relationship
from management_server.models.helpers import EmailString
from management_server.models.validators import phone_number_vaidator
from management_server.models import BaseModel, BaseUserModel


class UserModel(BaseUserModel, table=True):
    """
    User model class
    """

    model_config = ConfigDict(
        extra="forbid", str_strip_whitespace=True, use_enum_values=True
    )
    first_name: str = Field(max_length=20, min_length=3, nullable=False)
    last_name: str = Field(max_length=20, min_length=3, nullable=False)
    email: EmailString = Field(
        unique=True, nullable=False, max_length=255, min_length=15
    )
    phone_number: str = Field(unique=True, nullable=False, min_length=11, max_length=11)
    mobile_network: str = Field(
        nullable=False, min_length=4, max_length=15, default=None
    )
    state: str = Field(default=None, max_length=50, nullable=False)
    lga: str = Field(default=None, max_length=50, nullable=False)
    ward: str = Field(default=None, max_length=50, nullable=False)

    @property
    def full_name(self):
        """
        Returns the full name of the object.

        Returns:
            str: The full name of the object.
        """
        return f"{self.first_name} {self.last_name}"

    @model_validator(mode="before")
    def vaidate_user_model(self, data: Dict):
        """
        Validates the user model before saving it to the database.

        This function is a model validator that is called before saving the user model to the database.
        It performs the following checks:
        - Checks if the 'phone_number' field is empty and raises an assertion error if it is.
        - Checks if the 'mobile_network' field is empty and raises an assertion error if it is.
        - Validates the 'phone_number' field using the 'phone_number_vaidator' function and assigns the result to the 'validate' variable.
        - If the 'validate' variable is None, it raises an error (TODO).
        - Updates the 'mobile_network' field in the data dictionary with the value from the 'validate.network' attribute.

        Parameters:
            data (Dict): The data dictionary containing the user model data.

        Returns:
            Dict: The updated data dictionary with the 'mobile_network' field updated.
        """
        user_phone_number = self.get("phone_numeber", None)
        mobile_network = self.get("mobile_network", None)
        assert user_phone_number is None, "Field phone_numeber is empty"

        assert mobile_network is None, "Field mobile_network is empty"

        validate = phone_number_vaidator(phone_number=user_phone_number)
        if validate is None:
            # TODO raise an error here
            pass
        return data.update(("mobile_network", validate.network))


class DepartmentModel(BaseModel, table=True):
    department_id: str = Field(
        default=None, primary_key=True, nullable=False, index=True
    )
    name: str = Field(max_length=20, min_length=3, nullable=False, unique=True)
    short_name: str = Field(max_length=3, min_length=3, nullable=False, unique=True)
    description: str
    department_head: str


class StaffModel(BaseModel, table=True):
    staff_id: str = Field(default=None, primary_key=True, nullable=False, index=True)
    user_id: str
    deapartment_head: str
    department_id: str


class AdminModel(StaffModel, table=True):
    pass
